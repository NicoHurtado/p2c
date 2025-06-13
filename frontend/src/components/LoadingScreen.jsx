import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, BookOpen, Sparkles, Lightbulb, Target, Zap } from 'lucide-react';

const LoadingScreen = () => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { icon: Brain, text: "Analizando tu solicitud", color: "#4f46e5" },
    { icon: Lightbulb, text: "Generando ideas personalizadas", color: "#06b6d4" },
    { icon: Target, text: "Estructurando módulos", color: "#10b981" },
    { icon: BookOpen, text: "Creando contenido educativo", color: "#f59e0b" },
    { icon: Sparkles, text: "Añadiendo toques finales", color: "#ef4444" }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) return 100;
        return prev + 2;
      });
    }, 100);

    const stepInterval = setInterval(() => {
      setCurrentStep(prev => (prev + 1) % steps.length);
    }, 2000);

    return () => {
      clearInterval(interval);
      clearInterval(stepInterval);
    };
  }, []);

  const LoadingIcon = ({ icon: Icon, color, isActive }) => (
    <motion.div
      initial={{ scale: 0.8, opacity: 0.5 }}
      animate={{ 
        scale: isActive ? 1.2 : 0.8, 
        opacity: isActive ? 1 : 0.5,
        rotate: isActive ? 360 : 0
      }}
      transition={{ duration: 0.5, ease: "easeInOut" }}
      style={{
        background: isActive ? color : '#e5e7eb',
        borderRadius: '16px',
        padding: '16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: isActive ? `0 8px 25px ${color}40` : 'none'
      }}
    >
      <Icon size={32} color={isActive ? 'white' : '#9ca3af'} />
    </motion.div>
  );

  return (
    <div className="container" style={{ 
      paddingTop: '4rem', 
      paddingBottom: '4rem',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '70vh'
    }}>
      <div className="card" style={{ 
        maxWidth: '600px', 
        width: '100%',
        textAlign: 'center'
      }}>
        <div className="card-body" style={{ padding: '3rem' }}>
          {/* Main loading animation */}
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            style={{ marginBottom: '2rem' }}
          >
            <div style={{
              background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
              borderRadius: '20px',
              padding: '24px',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1.5rem'
            }}>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <Zap size={40} color="white" />
              </motion.div>
            </div>
            
            <h2 className="text-2xl font-bold mb-4">
              Creando tu curso personalizado
            </h2>
            
            <p className="text-gray-600 mb-6">
              Nuestra IA está trabajando para diseñar un curso único adaptado a tus necesidades
            </p>
          </motion.div>

          {/* Progress bar */}
          <div style={{
            background: '#f3f4f6',
            borderRadius: '12px',
            height: '12px',
            marginBottom: '2rem',
            overflow: 'hidden'
          }}>
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              style={{
                height: '100%',
                background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
                borderRadius: '12px'
              }}
            />
          </div>

          {/* Progress percentage */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-lg font-semibold text-primary mb-6"
          >
            {progress}%
          </motion.div>

          {/* Step indicators */}
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '1rem',
            marginBottom: '2rem',
            flexWrap: 'wrap'
          }}>
            {steps.map((step, index) => (
              <LoadingIcon
                key={index}
                icon={step.icon}
                color={step.color}
                isActive={index === currentStep}
              />
            ))}
          </div>

          {/* Current step text */}
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="text-gray-700 font-medium"
          >
            {steps[currentStep].text}
          </motion.div>

          {/* Fun facts */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.5 }}
            style={{
              marginTop: '2rem',
              padding: '1.5rem',
              background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
              borderRadius: '12px',
              border: '1px solid #e2e8f0'
            }}
          >
            <div className="text-sm text-gray-600">
              <Sparkles size={16} style={{ display: 'inline', marginRight: '0.5rem', color: '#f59e0b' }} />
              <strong>¿Sabías que?</strong> Los cursos personalizados mejoran el aprendizaje hasta en un 80%
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen; 