import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import CourseForm from './components/CourseForm';
import LoadingScreen from './components/LoadingScreen';
import CourseDisplay from './components/CourseDisplay';
import ModuleViewer from './components/ModuleViewer';

function App() {
  const [currentStep, setCurrentStep] = useState('form'); // 'form', 'loading', 'course', 'module'
  const [courseData, setCourseData] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);

  const handleCourseGeneration = async (formData) => {
    setIsGenerating(true);
    setCurrentStep('loading');

    try {
      console.log('📤 Enviando petición con datos:', formData);
      
      const response = await fetch('/api/courses/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      console.log('📥 Respuesta recibida:', response.status, response.statusText);

      if (!response.ok) {
        // Intentar obtener el mensaje de error específico
        let errorMessage = 'Error generando el curso';
        try {
          const errorData = await response.json();
          console.error('❌ Error del servidor:', errorData);
          
          if (response.status === 422) {
            errorMessage = 'Error de validación: ';
            if (errorData.detail) {
              if (typeof errorData.detail === 'string') {
                errorMessage += errorData.detail;
              } else if (Array.isArray(errorData.detail)) {
                errorMessage += errorData.detail.map(err => err.msg).join(', ');
              } else {
                errorMessage += 'Datos del formulario inválidos';
              }
            } else {
              errorMessage += 'Por favor verifica que todos los campos estén completos y correctos';
            }
          } else {
            errorMessage = errorData.detail || errorData.message || errorMessage;
          }
        } catch (parseError) {
          console.error('❌ Error parseando respuesta de error:', parseError);
        }
        
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log('📚 Course data received:', data);
      console.log('📚 Course ID:', data.course_id);
      console.log('📚 Metadata:', data.metadata);
      
      // Verificar que tenemos los datos necesarios
      if (!data.course_id || !data.metadata) {
        throw new Error('Respuesta incompleta del servidor');
      }
      
      setCourseData(data);
      console.log('📚 Course data set in state');
      
      // Reducir el delay y agregar más logging
      setTimeout(() => {
        console.log('📚 About to transition to course display step');
        console.log('📚 Current courseData:', data);
        setCurrentStep('course');
        setIsGenerating(false);
        console.log('📚 Transition completed - should now show course');
      }, 800); // Reducido de 1500 a 800ms

    } catch (error) {
      console.error('❌ Error completo:', error);
      setIsGenerating(false);
      setCurrentStep('form');
      
      // Mostrar mensaje de error más específico
      alert(`❌ ${error.message}\n\nPor favor verifica:\n• Que la descripción no esté vacía\n• Que hayas seleccionado un nivel\n• Que tengas conexión a internet`);
    }
  };

  const handleStartNew = () => {
    setCurrentStep('form');
    setCourseData(null);
    setIsGenerating(false);
    setCurrentModuleIndex(0);
  };

  const handleModuleStart = (moduleIndex) => {
    setCurrentModuleIndex(moduleIndex);
    setCurrentStep('module');
  };

  const handleBackToCourse = () => {
    setCurrentStep('course');
  };

  const handleNextModule = () => {
    if (courseData && currentModuleIndex < courseData.metadata.total_modules - 1) {
      setCurrentModuleIndex(currentModuleIndex + 1);
    } else {
      handleBackToCourse();
    }
  };

  const handlePrevModule = () => {
    if (currentModuleIndex > 0) {
      setCurrentModuleIndex(currentModuleIndex - 1);
    }
  };

  const handleForceComplete = () => {
    console.log('🔧 Force completing with courseData:', courseData);
    if (courseData) {
      setCurrentStep('course');
      setIsGenerating(false);
    }
  };

  return (
    <div className="App">
      <Header />
      
      <main>
        <AnimatePresence mode="wait">
          {currentStep === 'form' && (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <CourseForm onSubmit={handleCourseGeneration} isLoading={isGenerating} />
            </motion.div>
          )}

          {currentStep === 'loading' && (
            <motion.div
              key="loading"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.1 }}
              transition={{ duration: 0.6 }}
            >
              <LoadingScreen onForceComplete={courseData ? handleForceComplete : null} />
            </motion.div>
          )}

          {currentStep === 'course' && courseData && (
            <motion.div
              key="course"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -30 }}
              transition={{ duration: 0.7, ease: "easeOut" }}
            >
              <CourseDisplay 
                courseData={courseData} 
                onStartNew={handleStartNew}
                onModuleStart={handleModuleStart}
              />
            </motion.div>
          )}

          {currentStep === 'module' && courseData && (
            <motion.div
              key="module"
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -30 }}
              transition={{ duration: 0.6, ease: "easeOut" }}
            >
              <ModuleViewer
                courseId={courseData.course_id}
                moduleIndex={currentModuleIndex}
                totalModules={courseData.metadata.total_modules}
                onBack={handleBackToCourse}
                onNextModule={currentModuleIndex < courseData.metadata.total_modules - 1 ? handleNextModule : null}
                onPrevModule={currentModuleIndex > 0 ? handlePrevModule : null}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App; 