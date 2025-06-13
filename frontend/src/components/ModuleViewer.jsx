import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, 
  ArrowRight, 
  BookOpen, 
  CheckCircle, 
  PlayCircle,
  Users,
  Clock,
  Target,
  Lightbulb,
  Award,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const ModuleViewer = ({ courseId, moduleIndex, totalModules, onBack, onNextModule, onPrevModule }) => {
  const [moduleData, setModuleData] = useState(null);
  const [currentChunk, setCurrentChunk] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    const fetchModuleData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // Obtener el curso completo
        const response = await fetch(`/api/courses/${courseId}`);
        if (!response.ok) {
          throw new Error('Error cargando el curso');
        }
        
        const courseData = await response.json();
        const module = courseData.modules[moduleIndex];
        
        if (!module) {
          // Si el módulo no existe, generarlo bajo demanda
          console.log(`Módulo ${moduleIndex + 1} no existe, generando...`);
          setIsGenerating(true);
          
          const generateResponse = await fetch(`/api/courses/${courseId}/generate-module/${moduleIndex}`, {
            method: 'POST'
          });
          
          if (!generateResponse.ok) {
            throw new Error('Error generando el módulo');
          }
          
          const generateData = await generateResponse.json();
          setModuleData(generateData.module);
          setIsGenerating(false);
        } else {
          setModuleData(module);
        }
        
        setCurrentChunk(0);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    if (courseId && moduleIndex !== undefined) {
      fetchModuleData();
    }
  }, [courseId, moduleIndex]);

  const nextChunk = () => {
    if (moduleData && currentChunk < moduleData.chunks.length - 1) {
      setCurrentChunk(currentChunk + 1);
    }
  };

  const prevChunk = () => {
    if (currentChunk > 0) {
      setCurrentChunk(currentChunk - 1);
    }
  };

  if (isLoading) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <div className="card-body text-center" style={{ padding: '3rem' }}>
            <div className="loading-spinner" style={{ margin: '0 auto 1rem', width: '40px', height: '40px' }}></div>
            <p className="text-gray-600">
              {isGenerating 
                ? `🤖 Generando módulo ${moduleIndex + 1} con IA...` 
                : 'Cargando módulo...'
              }
            </p>
            {isGenerating && (
              <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>
                Esto puede tomar unos segundos mientras Claude crea el contenido personalizado
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <div className="card-body text-center" style={{ padding: '3rem' }}>
            <p className="text-red-600 mb-4">❌ {error}</p>
            <button onClick={onBack} className="btn btn-secondary">
              <ArrowLeft size={16} />
              Volver al Curso
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!moduleData) {
    return null;
  }

  const currentChunkData = moduleData.chunks[currentChunk];
  const progress = ((currentChunk + 1) / moduleData.chunks.length) * 100;

  return (
    <div className="module-viewer">
      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
        color: 'white',
        padding: '1.5rem 0'
      }}>
        <div className="container">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <button 
              onClick={onBack}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                color: 'white',
                padding: '0.5rem',
                borderRadius: '8px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}
            >
              <ArrowLeft size={16} />
              Volver
            </button>
            
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '0.875rem', opacity: 0.8, marginBottom: '0.25rem' }}>
                Módulo {moduleIndex + 1} de {totalModules}
              </div>
              <h1 style={{ fontSize: '1.5rem', fontWeight: '600', margin: 0 }}>
                {moduleData.title}
              </h1>
            </div>
          </div>

          {/* Progress Bar */}
          <div style={{
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '10px',
            height: '8px',
            overflow: 'hidden'
          }}>
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
              style={{
                height: '100%',
                background: 'white',
                borderRadius: '10px'
              }}
            />
          </div>
          
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginTop: '0.5rem',
            fontSize: '0.875rem',
            opacity: 0.9
          }}>
            <span>Progreso: {Math.round(progress)}%</span>
            <span>Sección {currentChunk + 1} de {moduleData.chunks.length}</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          {/* Module Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card mb-6"
          >
            <div className="card-body">
              <div style={{ marginBottom: '1.5rem' }}>
                <h3 style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.5rem',
                  margin: '0 0 0.5rem 0'
                }}>
                  <Target size={20} style={{ color: '#4f46e5' }} />
                  Objetivo del Módulo
                </h3>
                <p className="text-gray-600">{moduleData.objective}</p>
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <h4 style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.5rem',
                  margin: '0 0 0.5rem 0'
                }}>
                  <Lightbulb size={16} style={{ color: '#f59e0b' }} />
                  Conceptos Clave
                </h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                  {moduleData.concepts.map((concept, index) => (
                    <span
                      key={index}
                      style={{
                        padding: '0.25rem 0.75rem',
                        background: '#f3f4f6',
                        borderRadius: '15px',
                        fontSize: '0.875rem',
                        color: '#4b5563'
                      }}
                    >
                      {concept}
                    </span>
                  ))}
                </div>
              </div>

              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '1rem',
                padding: '1rem',
                background: '#f8fafc',
                borderRadius: '8px'
              }}>
                <div style={{ textAlign: 'center' }}>
                  <Clock size={24} style={{ color: '#06b6d4', margin: '0 auto 0.5rem' }} />
                  <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>Duración</div>
                  <div style={{ fontWeight: '600' }}>~2h</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <Users size={24} style={{ color: '#10b981', margin: '0 auto 0.5rem' }} />
                  <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>Estudiantes</div>
                  <div style={{ fontWeight: '600' }}>{Math.floor(Math.random() * 500) + 200}+</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <Award size={24} style={{ color: '#f59e0b', margin: '0 auto 0.5rem' }} />
                  <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>Secciones</div>
                  <div style={{ fontWeight: '600' }}>{moduleData.chunks.length}</div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Content Chunk */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentChunk}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="card"
            >
              <div className="card-body">
                <div style={{
                  minHeight: '400px',
                  padding: '1rem',
                  fontSize: '1rem',
                  lineHeight: '1.7',
                  whiteSpace: 'pre-wrap'
                }}>
                  {currentChunkData?.content || 'Contenido no disponible'}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: '2rem',
            padding: '1rem',
            background: '#f8fafc',
            borderRadius: '12px'
          }}>
            <button
              onClick={prevChunk}
              disabled={currentChunk === 0}
              className="btn btn-secondary"
              style={{ 
                opacity: currentChunk === 0 ? 0.5 : 1,
                cursor: currentChunk === 0 ? 'not-allowed' : 'pointer'
              }}
            >
              <ChevronLeft size={16} />
              Anterior
            </button>

            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.25rem' }}>
                Sección {currentChunk + 1} de {moduleData.chunks.length}
              </div>
              <div style={{ display: 'flex', gap: '0.25rem', justifyContent: 'center' }}>
                {moduleData.chunks.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentChunk(index)}
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      border: 'none',
                      background: index === currentChunk ? '#4f46e5' : '#d1d5db',
                      cursor: 'pointer'
                    }}
                  />
                ))}
              </div>
            </div>

            <button
              onClick={nextChunk}
              disabled={currentChunk === moduleData.chunks.length - 1}
              className="btn btn-primary"
              style={{ 
                opacity: currentChunk === moduleData.chunks.length - 1 ? 0.5 : 1,
                cursor: currentChunk === moduleData.chunks.length - 1 ? 'not-allowed' : 'pointer'
              }}
            >
              Siguiente
              <ChevronRight size={16} />
            </button>
          </div>

          {/* Module Navigation */}
          {(onPrevModule || onNextModule) && (
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: '2rem',
              padding: '1.5rem',
              background: 'white',
              borderRadius: '12px',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
              border: '1px solid #e5e7eb'
            }}>
              {onPrevModule ? (
                <button onClick={onPrevModule} className="btn btn-secondary">
                  <ArrowLeft size={16} />
                  Módulo Anterior
                </button>
              ) : <div></div>}

              {onNextModule ? (
                <button onClick={onNextModule} className="btn btn-primary">
                  Módulo Siguiente
                  <ArrowRight size={16} />
                </button>
              ) : (
                <button onClick={onBack} className="btn btn-primary">
                  <CheckCircle size={16} />
                  Completar Curso
                </button>
              )}
            </div>
          )}

          {/* Module Summary */}
          {currentChunk === moduleData.chunks.length - 1 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ marginTop: '2rem' }}
            >
              <div className="card" style={{
                background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
                color: 'white',
                border: 'none'
              }}>
                <div className="card-body text-center">
                  <CheckCircle size={32} style={{ margin: '0 auto 1rem' }} />
                  <h4 style={{ margin: '0 0 1rem 0' }}>
                    🎉 ¡Módulo Completado!
                  </h4>
                  <p style={{ opacity: 0.9, margin: 0 }}>
                    Has terminado "{moduleData.title}". ¡Excelente trabajo!
                  </p>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ModuleViewer; 