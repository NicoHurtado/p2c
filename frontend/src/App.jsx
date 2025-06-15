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
      const response = await fetch('/api/courses/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Error generating course');
      }

      const data = await response.json();
      console.log('📚 Course data received:', data);
      console.log('📚 Course ID:', data.course_id);
      console.log('📚 Metadata:', data.metadata);
      
      setCourseData(data);
      
      // Simular un pequeño delay para mostrar la animación de carga
      setTimeout(() => {
        console.log('📚 Transitioning to course display step');
        setCurrentStep('course');
        setIsGenerating(false);
      }, 1500);

    } catch (error) {
      console.error('Error:', error);
      setIsGenerating(false);
      setCurrentStep('form');
      alert('Hubo un error generando el curso. Por favor intenta de nuevo.');
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
              <LoadingScreen />
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