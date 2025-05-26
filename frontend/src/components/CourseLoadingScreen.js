import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiCamera, FiBook, FiStar, FiZap, FiHeart, FiCoffee, FiClock } from 'react-icons/fi';

const CourseLoadingScreen = ({ isVisible, progress = 0 }) => {
  const [currentMessage, setCurrentMessage] = useState(0);
  const [dots, setDots] = useState('');
  const [elapsedTime, setElapsedTime] = useState(0);

  const loadingMessages = [
    "🤖 Analizando tu perfil de aprendizaje...",
    "📚 Consultando bases de conocimiento...",
    "🎯 Ajustando el contenido a tu nivel...",
    "✨ Generando módulos personalizados...",
    "🎨 Diseñando ejercicios prácticos...",
    "📖 Creando recursos de aprendizaje...",
    "🧠 Optimizando la secuencia didáctica...",
    "🚀 Preparando tu asistente virtual...",
    "🔍 Revisando calidad del contenido...",
    "🎉 ¡Casi listo! Finalizando tu curso..."
  ];

  const timeBasedMessages = [
    { time: 0, message: "🚀 Iniciando generación..." },
    { time: 30, message: "⏳ Esto puede tomar varios minutos..." },
    { time: 60, message: "🧠 La IA está trabajando en tu curso..." },
    { time: 120, message: "📚 Creando contenido de calidad..." },
    { time: 180, message: "✨ Perfeccionando los detalles..." },
    { time: 300, message: "🎯 Casi terminado, ten paciencia..." },
    { time: 420, message: "🔥 Generando un curso increíble..." },
    { time: 600, message: "💎 Puliendo los últimos detalles..." }
  ];

  useEffect(() => {
    if (!isVisible) {
      setElapsedTime(0);
      return;
    }

    // Timer for elapsed time
    const timeInterval = setInterval(() => {
      setElapsedTime(prev => prev + 1);
    }, 1000);

    // Message rotation
    const messageInterval = setInterval(() => {
      setCurrentMessage((prev) => (prev + 1) % loadingMessages.length);
    }, 3000);

    // Dots animation
    const dotsInterval = setInterval(() => {
      setDots((prev) => {
        if (prev === '...') return '';
        return prev + '.';
      });
    }, 500);

    return () => {
      clearInterval(timeInterval);
      clearInterval(messageInterval);
      clearInterval(dotsInterval);
    };
  }, [isVisible]);

  // Get time-based message
  const getTimeBasedMessage = () => {
    const applicableMessages = timeBasedMessages.filter(msg => elapsedTime >= msg.time);
    return applicableMessages.length > 0 
      ? applicableMessages[applicableMessages.length - 1].message 
      : timeBasedMessages[0].message;
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!isVisible) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center"
    >
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl">
        {/* Animated Character */}
        <div className="flex justify-center mb-6">
          <motion.div
            animate={{
              rotate: [0, 10, -10, 0],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="text-6xl"
          >
            🤖
          </motion.div>
        </div>

        {/* Loading Message */}
        <motion.div
          key={currentMessage}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="text-center mb-6"
        >
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
            Generando tu curso personalizado
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-2">
            {loadingMessages[currentMessage]}{dots}
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {getTimeBasedMessage()}
          </p>
        </motion.div>

        {/* Timer and Progress */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-500 dark:text-gray-400 mb-2">
            <span className="flex items-center gap-1">
              <FiClock size={14} />
              {formatTime(elapsedTime)}
            </span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Floating Icons */}
        <div className="flex justify-center space-x-4 mb-4">
          {[FiCamera, FiBook, FiStar, FiZap, FiHeart, FiCoffee].map((Icon, index) => (
            <motion.div
              key={index}
              animate={{
                y: [0, -10, 0],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: index * 0.3,
              }}
              className="text-blue-500 dark:text-blue-400"
            >
              <Icon size={20} />
            </motion.div>
          ))}
        </div>

        {/* Fun Facts */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-center text-sm text-gray-500 dark:text-gray-400"
        >
          💡 <strong>Dato curioso:</strong> La IA está analizando miles de recursos para crear tu curso perfecto
        </motion.div>

        {/* Time warning for long generations */}
        {elapsedTime > 120 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg"
          >
            <p className="text-sm text-yellow-800 dark:text-yellow-200 text-center">
              ⏰ Las generaciones complejas pueden tomar hasta 10-15 minutos. ¡Tu curso será increíble!
            </p>
          </motion.div>
        )}

        {/* Pulsing Dots */}
        <div className="flex justify-center mt-4 space-x-1">
          {[0, 1, 2].map((index) => (
            <motion.div
              key={index}
              className="w-2 h-2 bg-blue-500 rounded-full"
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.5, 1, 0.5],
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                delay: index * 0.2,
              }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
};

export default CourseLoadingScreen; 