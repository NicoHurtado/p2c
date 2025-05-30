import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSearch, FiClock, FiBookOpen, FiChevronRight, FiAward, FiCheck, FiCode, FiServer, FiLayers, FiCpu, FiCamera, FiWind, FiEdit3, FiDatabase, FiCloud } from 'react-icons/fi';

const AnimatedSearch = () => {
  const [searchPhase, setSearchPhase] = useState('initial'); // initial, typing, searching, results
  const [searchText, setSearchText] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  const searchTextRef = useRef('');
  const searchPhrases = [
    'Quiero aprender sobre inteligencia artificial',
    'Aprender sobre fotografía urbana',
    'Curso avanzado de desarrollo web'
  ];
  const selectedPhrase = useRef(searchPhrases[0]);
  const phraseIndex = useRef(0);
  
  const courseResultsData = [ // Renamed and expanded
    { // AI Course
      title: 'Fundamentos de Inteligencia Artificial',
      level: 'Principiante',
      duration: '3 horas',
      modules: [
        { title: 'Introducción a la IA', lessons: 3, duration: '45 min', icon: <FiCpu /> },
        { title: 'Algoritmos básicos', lessons: 4, duration: '60 min', icon: <FiCode /> },
        { title: 'Procesamiento de datos', lessons: 5, duration: '75 min', icon: <FiServer /> }
      ]
    },
    { // Urban Photography Course
      title: 'Fotografía Urbana Creativa',
      level: 'Intermedio',
      duration: '4 horas',
      modules: [
        { title: 'Composición en la Calle', lessons: 4, duration: '60 min', icon: <FiCamera /> },
        { title: 'Capturando el Movimiento', lessons: 3, duration: '50 min', icon: <FiWind /> },
        { title: 'Edición para Impacto Visual', lessons: 5, duration: '90 min', icon: <FiEdit3 /> },
        { title: 'Narrativa Fotográfica', lessons: 3, duration: '40 min', icon: <FiBookOpen /> }
      ]
    },
    { // Web Development Course
      title: 'Desarrollo Web Full-Stack con React y Node.js',
      level: 'Avanzado',
      duration: '10 horas',
      modules: [
        { title: 'React Avanzado y State Management', lessons: 6, duration: '120 min', icon: <FiLayers /> },
        { title: 'APIs con Node.js y Express', lessons: 5, duration: '100 min', icon: <FiServer /> },
        { title: 'Bases de Datos NoSQL con MongoDB', lessons: 4, duration: '80 min', icon: <FiDatabase /> },
        { title: 'Despliegue y DevOps', lessons: 3, duration: '60 min', icon: <FiCloud /> }
      ]
    }
  ];
  
  const [currentCourseResult, setCurrentCourseResult] = useState(courseResultsData[0]); // State for current course

  // Efecto para la animación de escritura
  useEffect(() => {
    if (searchPhase === 'initial') {
      // Comenzar a escribir después de 1 segundo
      const timeout = setTimeout(() => {
        setSearchPhase('typing');
        setShowCursor(true);
      }, 1000);
      return () => clearTimeout(timeout);
    }
    
    if (searchPhase === 'typing') {
      // Simular escritura del texto
      if (searchTextRef.current.length < selectedPhrase.current.length) {
        const typingTimeout = setTimeout(() => {
          const nextChar = selectedPhrase.current[searchTextRef.current.length];
          searchTextRef.current += nextChar;
          setSearchText(searchTextRef.current);
          
          // Parpadeo del cursor
          const cursorTimeout = setTimeout(() => {
            setShowCursor(prev => !prev);
          }, 100);
          
          return () => clearTimeout(cursorTimeout);
        }, Math.random() * 100 + 50); // Velocidad de escritura variable
        
        return () => clearTimeout(typingTimeout);
      } else {
        // Finalizar la escritura y empezar a buscar
        const searchStartTimeout = setTimeout(() => {
          setSearchPhase('searching');
        }, 500);
        
        return () => clearTimeout(searchStartTimeout);
      }
    }
    
    if (searchPhase === 'searching') {
      // Simular proceso de búsqueda por 2 segundos
      const searchingTimeout = setTimeout(() => {
        setCurrentCourseResult(courseResultsData[phraseIndex.current % courseResultsData.length]); // Update current course result
        setSearchPhase('results');
      }, 2000);
      
      return () => clearTimeout(searchingTimeout);
    }
    
    if (searchPhase === 'results') {
      // Mostrar resultados por 8 segundos y luego reiniciar
      const resetTimeout = setTimeout(() => {
        searchTextRef.current = '';
        setSearchText('');
        
        // Cambiar a la siguiente frase
        phraseIndex.current = (phraseIndex.current + 1) % searchPhrases.length;
        selectedPhrase.current = searchPhrases[phraseIndex.current];
        
        setSearchPhase('initial');
      }, 8000);
      
      return () => clearTimeout(resetTimeout);
    }
  }, [searchPhase, searchText]);
  
  // Renderizar los pulsos de búsqueda
  const renderSearchPulses = () => {
    return (
      <motion.div 
        className="ml-2 flex items-center" 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex gap-1">
          {[0, 1, 2].map((i) => (
            <motion.div 
              key={i}
              className="h-1.5 w-1.5 rounded-full bg-primary-400" 
              animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
              transition={{ 
                duration: 0.6, 
                repeat: Infinity, 
                repeatType: 'loop', 
                delay: i * 0.2 
              }}
            />
          ))}
        </div>
      </motion.div>
    );
  };
  
  return (
    <div className="w-full max-w-2xl mx-auto">
      <motion.div 
        className="rounded-2xl bg-white/60 backdrop-blur-xl p-2 border border-neutral-200/60 shadow-2xl overflow-hidden"
        initial={{ boxShadow: "0 0 0 rgba(56, 189, 248, 0)" }}
        animate={{ 
          boxShadow: searchPhase === 'searching' ? 
            "0 0 20px rgba(56, 189, 248, 0.1)" : 
            "0 0 0 rgba(56, 189, 248, 0)" 
        }}
        transition={{ duration: 0.8 }}
      >
        {/* Barra de búsqueda */}
        <div className="flex items-center px-4 py-3 relative">
          <motion.div
            animate={{ 
              color: searchPhase === 'searching' ? '#2563eb' : '#6b7280'
            }}
            transition={{ duration: 0.5 }}
          >
            <FiSearch className="mr-3 h-5 w-5" />
          </motion.div>
          
          <div className="flex-1 overflow-hidden">
            <div className="relative h-6 flex items-center">
              <motion.div 
                className="text-neutral-800 text-base font-medium flex items-center"
                initial={{ x: 0 }}
                animate={{ 
                  x: searchPhase === 'searching' ? -5 : 0
                }}
                transition={{ duration: 0.3, type: "spring" }}
              >
                {searchText}
                {showCursor && searchPhase !== 'results' && (
                  <span className="text-primary-500 opacity-70 ml-[1px]">|</span>
                )}
                
                {searchPhase === 'searching' && renderSearchPulses()}
              </motion.div>
            </div>
          </div>
          
          {/* Botón de búsqueda (visible después de terminar de escribir) */}
          <AnimatePresence>
            {searchPhase === 'searching' && (
              <motion.button 
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="ml-2 bg-primary-500/10 text-primary-600 h-8 w-8 rounded-full flex items-center justify-center"
              >
                <FiSearch className="h-4 w-4" />
              </motion.button>
            )}
          </AnimatePresence>
        </div>
        
        {/* Resultado de la búsqueda */}
        <AnimatePresence>
          {searchPhase === 'results' && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="border-t border-neutral-200/60 mt-1 pt-3 px-4 pb-3"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="text-sm text-neutral-500">Cursos encontrados (1)</div>
                <div className="flex items-center gap-1">
                  <div className="h-1.5 w-1.5 rounded-full bg-primary-500"></div>
                  <div className="text-xs text-neutral-500">Resultados en tiempo real</div>
                </div>
              </div>
              
              <motion.div 
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="bg-white/80 rounded-xl p-4 hover:bg-neutral-50 transition-colors cursor-pointer border border-neutral-200/50 overflow-hidden relative shadow-md"
              >
                {/* Efecto de brillo en la esquina */}
                <div className="absolute -top-10 -right-10 h-20 w-20 bg-primary-500/5 blur-2xl rounded-full"></div>
                
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-neutral-800 font-semibold text-lg">{currentCourseResult.title}</h3>
                    <p className="text-neutral-500 text-sm mt-1">{currentCourseResult.level} · {currentCourseResult.modules.length} módulos</p>
                  </div>
                  <div className="bg-primary-500/10 text-primary-600 text-xs rounded-lg px-2 py-1 flex items-center">
                    <FiClock className="mr-1" /> {currentCourseResult.duration}
                  </div>
                </div>
                
                <div className="mt-4 grid grid-cols-1 gap-3">
                  {currentCourseResult.modules.map((module, idx) => (
                    <motion.div 
                      key={idx} 
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 + (idx * 0.1) }}
                      className="flex items-center p-2 rounded-lg hover:bg-neutral-100/70 transition-colors"
                    >
                      <div className="w-8 h-8 rounded-full bg-primary-500/10 flex items-center justify-center text-primary-600 mr-3">
                        {module.icon}
                      </div>
                      <div className="flex-1">
                        <div className="text-neutral-700 font-medium">{module.title}</div>
                        <div className="text-neutral-500 text-xs">{module.lessons} lecciones · {module.duration}</div>
                      </div>
                      <motion.div 
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        className="w-6 h-6 rounded-full bg-neutral-200/50 flex items-center justify-center text-neutral-500"
                      >
                        <FiChevronRight size={14} />
                      </motion.div>
                    </motion.div>
                  ))}
                </div>
                
                <div className="mt-4 pt-3 border-t border-neutral-200/50 flex justify-between items-center">
                  <div className="flex items-center text-xs text-neutral-500">
                    <FiAward className="mr-1 text-primary-500" /> Certificado disponible
                  </div>
                  <motion.button 
                    whileHover={{ scale: 1.03 }}
                    whileTap={{ scale: 0.97 }}
                    className="flex items-center text-primary-600 text-sm bg-primary-500/10 px-3 py-1.5 rounded-lg hover:bg-primary-500/20 transition-colors border border-primary-500/30"
                  >
                    Ver curso
                    <FiChevronRight className="ml-1" />
                  </motion.button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

export default AnimatedSearch; 