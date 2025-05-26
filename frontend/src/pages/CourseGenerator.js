import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiCpu, FiArrowRight, FiCheck, FiInfo } from 'react-icons/fi';
import Layout from '../components/Layout';
import CourseLoadingScreen from '../components/CourseLoadingScreen';
import CourseDisplay from '../components/CourseDisplay';
import { courseService } from '../services/api';
import { ThemeContext } from '../context/ThemeContext';

const experienceLevels = [
  { id: 'beginner', name: 'Principiante', description: 'Poco o ningún conocimiento previo.' },
  { id: 'intermediate', name: 'Intermedio', description: 'Conceptos básicos y algo de experiencia.' },
  { id: 'advanced', name: 'Avanzado', description: 'Amplio conocimiento y experiencia.' },
];

const personalities = [
  { id: 'analytical', name: 'Analítico', description: 'Prefiero datos, lógica y análisis detallado.' },
  { id: 'creative', name: 'Creativo', description: 'Me gusta la innovación y el pensamiento fuera de la caja.' },
  { id: 'practical', name: 'Práctico', description: 'Enfoque directo y aplicación inmediata.' },
  { id: 'social', name: 'Social', description: 'Aprendo mejor en grupo y con interacción.' },
];

const learningStyles = [
  { id: 'visual', name: 'Visual', description: 'Aprendo mejor con imágenes, diagramas y gráficos.' },
  { id: 'auditory', name: 'Auditivo', description: 'Prefiero explicaciones verbales y discusiones.' },
  { id: 'kinesthetic', name: 'Kinestésico', description: 'Aprendo haciendo y con experiencias prácticas.' },
  { id: 'interactive', name: 'Interactivo', description: 'Prefiero ejercicios interactivos y gamificación.' },
];

const intensities = [
  { id: 'short', name: 'Corto', description: 'Curso rápido, conceptos esenciales (1-2 semanas).' },
  { id: 'medium', name: 'Medio', description: 'Curso balanceado con práctica (3-4 semanas).' },
  { id: 'long', name: 'Largo', description: 'Curso exhaustivo y detallado (2-3 meses).' },
];

const CourseGenerator = () => {
  const navigate = useNavigate();
  const { darkMode } = useContext(ThemeContext);
  
  const [prompt, setPrompt] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [personality, setPersonality] = useState('');
  const [learningStyle, setLearningStyle] = useState('');
  const [intensity, setIntensity] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [error, setError] = useState('');
  const [generatedCourse, setGeneratedCourse] = useState(null);
  const [showCourseDisplay, setShowCourseDisplay] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) {
      setError('Por favor, ingresa un tema para el curso');
      return;
    }
    
    if (!experienceLevel) {
      setError('Por favor, selecciona tu nivel de experiencia');
      return;
    }
    
    if (!personality) {
      setError('Por favor, selecciona tu tipo de personalidad');
      return;
    }
    
    if (!learningStyle) {
      setError('Por favor, selecciona tu estilo de aprendizaje');
      return;
    }
    
    if (!intensity) {
      setError('Por favor, selecciona la intensidad del curso');
      return;
    }
    
    setError('');
    setIsGenerating(true);
    setLoadingProgress(0);
    
    // More realistic progress simulation for long AI generations
    let currentProgress = 0;
    const progressInterval = setInterval(() => {
      setLoadingProgress(prev => {
        currentProgress = prev;
        
        // Slower, more realistic progress
        if (currentProgress < 20) {
          // Fast initial progress (connecting, validating)
          return prev + Math.random() * 8;
        } else if (currentProgress < 40) {
          // Slower progress (AI thinking)
          return prev + Math.random() * 3;
        } else if (currentProgress < 70) {
          // Very slow progress (generating content)
          return prev + Math.random() * 1.5;
        } else if (currentProgress < 85) {
          // Minimal progress (finalizing)
          return prev + Math.random() * 0.8;
        } else if (currentProgress < 95) {
          // Almost done
          return prev + Math.random() * 0.3;
        } else {
          // Stop at 95% until we get the response
          return 95;
        }
      });
    }, 2000); // Update every 2 seconds instead of 1
    
    try {
      const result = await courseService.generateCourse(
        prompt,
        experienceLevel,
        personality,
        learningStyle,
        intensity
      );
      
      clearInterval(progressInterval);
      setLoadingProgress(100);
      
      // Add form data to the result for saving
      const courseWithFormData = {
        ...result,
        prompt: prompt,
        experience_level: experienceLevel,
        personality: personality,
        learning_style: learningStyle,
        intensity: intensity
      };
      
      setGeneratedCourse(courseWithFormData);
      
      // Small delay to show 100% progress
      setTimeout(() => {
        setIsGenerating(false);
        setShowCourseDisplay(true);
      }, 1000);
      
    } catch (error) {
      clearInterval(progressInterval);
      console.error('Error generating course:', error);
      
      // Better error messages based on error type
      let errorMessage = 'Error al generar el curso. Por favor, intenta de nuevo.';
      
      if (error.message.includes('timeout') || error.message.includes('tiempo')) {
        errorMessage = 'La generación está tomando más tiempo del esperado. Esto es normal para cursos complejos. Por favor, intenta de nuevo o simplifica el tema.';
      } else if (error.message.includes('conexión') || error.message.includes('connect')) {
        errorMessage = 'No se puede conectar con el servicio de generación. Verifica que la API externa esté ejecutándose.';
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setError(errorMessage);
      setIsGenerating(false);
      setLoadingProgress(0);
    }
  };

  const handleSaveCourse = async () => {
    if (!generatedCourse) return;
    
    try {
      const courseData = {
        titulo: generatedCourse.titulo,
        prompt: generatedCourse.prompt,
        content: generatedCourse,
        experience_level: generatedCourse.experience_level,
        available_time: generatedCourse.duracion || intensity
      };
      
      const savedCourse = await courseService.saveCourse(courseData);
      
      // Close the display and redirect to the course view
      setShowCourseDisplay(false);
      navigate(`/courses/${savedCourse.id}`);
      
    } catch (error) {
      console.error('Error saving course:', error);
      setError('Error al guardar el curso. Por favor, intenta de nuevo.');
    }
  };

  const handleCloseCourseDisplay = () => {
    setShowCourseDisplay(false);
    setGeneratedCourse(null);
    setLoadingProgress(0);
  };
  
  // Clases dinámicas basadas en el tema
  const titleClass = darkMode ? 'text-white' : 'text-neutral-900';
  const subtitleClass = darkMode ? 'text-white' : 'text-neutral-900';
  const labelClass = darkMode ? 'text-white' : 'text-neutral-700';
  const hintTextClass = darkMode ? 'text-neutral-300' : 'text-neutral-500';
  
  // Clases para las tarjetas de selección
  const cardSelectedClass = darkMode 
    ? 'border-primary-500 bg-primary-900/30 ring-2 ring-primary-700'
    : 'border-primary-500 bg-primary-50 ring-2 ring-primary-200';
  
  const cardUnselectedClass = darkMode
    ? 'border-neutral-700 hover:border-primary-500'
    : 'border-neutral-200 hover:border-primary-300';
  
  // Clases para los textos en las tarjetas
  const cardTitleClass = darkMode ? 'text-white' : 'text-neutral-900';
  const cardDescriptionClass = darkMode ? 'text-neutral-300' : 'text-neutral-600';
  
  // Clase para los círculos numerados
  const circleClass = darkMode 
    ? 'flex items-center justify-center bg-primary-700 text-white w-8 h-8 rounded-full mr-3'
    : 'flex items-center justify-center bg-primary-100 text-primary-700 w-8 h-8 rounded-full mr-3';
  
  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        <h1 className={`text-2xl font-bold ${titleClass} mb-6`}>Generar curso</h1>
        
        {error && (
          <div className={`mb-6 ${darkMode 
            ? 'bg-red-900/20 border-red-800/30 text-red-400' 
            : 'bg-red-50 border-red-200 text-red-700'} 
            border px-4 py-3 rounded-lg`} role="alert">
            <span>{error}</span>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Topic section */}
          <div className="card">
            <h2 className={`text-lg font-medium ${subtitleClass} mb-4 flex items-center`}>
              <span className={circleClass}>1</span>
              ¿Qué quieres aprender?
            </h2>
            
            <div>
              <label htmlFor="prompt" className={`block text-sm font-medium ${labelClass} mb-1`}>
                Tema o habilidad
              </label>
              <textarea
                id="prompt"
                name="prompt"
                rows={3}
                className="input"
                placeholder="Describe el tema que quieres aprender. Sé específico para obtener mejores resultados."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
              <p className={`mt-2 text-sm ${hintTextClass}`}>
                <FiInfo className="inline mr-1" />
                Ejemplos: "Programación en Python para análisis de datos", "Marketing digital para pequeños negocios"
              </p>
            </div>
          </div>
          
          {/* Experience level section */}
          <div className="card">
            <h2 className={`text-lg font-medium ${subtitleClass} mb-4 flex items-center`}>
              <span className={circleClass}>2</span>
              ¿Cuál es tu nivel de experiencia?
            </h2>
            
            <div className="grid gap-4 sm:grid-cols-3">
              {experienceLevels.map((level) => (
                <div 
                  key={level.id}
                  className={`border rounded-xl p-4 cursor-pointer transition-all duration-200 ${
                    experienceLevel === level.id 
                      ? cardSelectedClass
                      : cardUnselectedClass
                  }`}
                  onClick={() => setExperienceLevel(level.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className={`font-medium ${cardTitleClass}`}>{level.name}</h3>
                    {experienceLevel === level.id && (
                      <FiCheck className="text-primary-400" />
                    )}
                  </div>
                  <p className={`text-sm ${cardDescriptionClass}`}>{level.description}</p>
                </div>
              ))}
            </div>
          </div>
          
          {/* Personality section */}
          <div className="card">
            <h2 className={`text-lg font-medium ${subtitleClass} mb-4 flex items-center`}>
              <span className={circleClass}>3</span>
              ¿Cuál es tu tipo de personalidad?
            </h2>
            
            <div className="grid gap-4 sm:grid-cols-2">
              {personalities.map((pers) => (
                <div 
                  key={pers.id}
                  className={`border rounded-xl p-4 cursor-pointer transition-all duration-200 ${
                    personality === pers.id 
                      ? cardSelectedClass
                      : cardUnselectedClass
                  }`}
                  onClick={() => setPersonality(pers.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className={`font-medium ${cardTitleClass}`}>{pers.name}</h3>
                    {personality === pers.id && (
                      <FiCheck className="text-primary-400" />
                    )}
                  </div>
                  <p className={`text-sm ${cardDescriptionClass}`}>{pers.description}</p>
                </div>
              ))}
            </div>
          </div>
          
          {/* Learning style section */}
          <div className="card">
            <h2 className={`text-lg font-medium ${subtitleClass} mb-4 flex items-center`}>
              <span className={circleClass}>4</span>
              ¿Cuál es tu estilo de aprendizaje?
            </h2>
            
            <div className="grid gap-4 sm:grid-cols-2">
              {learningStyles.map((style) => (
                <div 
                  key={style.id}
                  className={`border rounded-xl p-4 cursor-pointer transition-all duration-200 ${
                    learningStyle === style.id 
                      ? cardSelectedClass
                      : cardUnselectedClass
                  }`}
                  onClick={() => setLearningStyle(style.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className={`font-medium ${cardTitleClass}`}>{style.name}</h3>
                    {learningStyle === style.id && (
                      <FiCheck className="text-primary-400" />
                    )}
                  </div>
                  <p className={`text-sm ${cardDescriptionClass}`}>{style.description}</p>
                </div>
              ))}
            </div>
          </div>
          
          {/* Intensity section */}
          <div className="card">
            <h2 className={`text-lg font-medium ${subtitleClass} mb-4 flex items-center`}>
              <span className={circleClass}>5</span>
              ¿Qué intensidad prefieres?
            </h2>
            
            <div className="grid gap-4 sm:grid-cols-3">
              {intensities.map((int) => (
                <div 
                  key={int.id}
                  className={`border rounded-xl p-4 cursor-pointer transition-all duration-200 ${
                    intensity === int.id 
                      ? cardSelectedClass
                      : cardUnselectedClass
                  }`}
                  onClick={() => setIntensity(int.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className={`font-medium ${cardTitleClass}`}>{int.name}</h3>
                    {intensity === int.id && (
                      <FiCheck className="text-primary-400" />
                    )}
                  </div>
                  <p className={`text-sm ${cardDescriptionClass}`}>{int.description}</p>
                </div>
              ))}
            </div>
          </div>
          
          {/* Submit button */}
          <div className="flex justify-end">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              disabled={isGenerating}
              className={`btn btn-primary py-3 px-6 ${isGenerating ? 'opacity-75 cursor-not-allowed' : ''}`}
            >
              {isGenerating ? (
                <div className="flex items-center">
                  <FiCpu className="animate-pulse mr-2" />
                  <span>Generando curso...</span>
                </div>
              ) : (
                <div className="flex items-center">
                  <span>Generar curso</span>
                  <FiArrowRight className="ml-2" />
                </div>
              )}
            </motion.button>
          </div>
        </form>
      </div>

      {/* Loading Screen */}
      <CourseLoadingScreen 
        isVisible={isGenerating} 
        progress={loadingProgress}
      />

      {/* Course Display */}
      {showCourseDisplay && generatedCourse && (
        <CourseDisplay
          course={generatedCourse}
          onSave={handleSaveCourse}
          onClose={handleCloseCourseDisplay}
          darkMode={darkMode}
        />
      )}
    </Layout>
  );
};

export default CourseGenerator; 