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
  ChevronRight,
  Video,
  AlertCircle
} from 'lucide-react';
import YouTubePlayer from './YouTubePlayer';
import MarkdownRenderer from './MarkdownRenderer';

const ModuleViewer = ({ courseId, moduleIndex, totalModules, onBack, onNextModule, onPrevModule }) => {
  const [moduleData, setModuleData] = useState(null);
  const [currentChunk, setCurrentChunk] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [debugInfo, setDebugInfo] = useState(null);

  // 🎨 STYLES - Pure CSS objects to replace Tailwind
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)',
    },
    header: {
      background: 'white',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
      borderBottom: '1px solid #e2e8f0'
    },
    headerContent: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '1rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    },
    headerLeft: {
      display: 'flex',
      alignItems: 'center',
      gap: '1rem'
    },
    backButton: {
      background: '#f1f5f9',
      border: 'none',
      color: '#374151',
      padding: '0.5rem',
      borderRadius: '0.5rem',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    title: {
      fontSize: '1.25rem',
      fontWeight: 'bold',
      color: '#111827',
      margin: 0
    },
    subtitle: {
      fontSize: '0.875rem',
      color: '#6b7280',
      margin: 0
    },
    progressContainer: {
      display: 'flex',
      alignItems: 'center',
      gap: '1rem'
    },
    progressText: {
      fontSize: '0.875rem',
      color: '#6b7280'
    },
    progressBar: {
      width: '8rem',
      height: '0.5rem',
      background: '#e5e7eb',
      borderRadius: '9999px',
      overflow: 'hidden'
    },
    progressFill: {
      height: '100%',
      background: '#2563eb',
      borderRadius: '9999px',
      transition: 'width 0.3s ease'
    },
    mainContent: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '1.5rem',
      display: 'grid',
      gridTemplateColumns: '1fr 300px',
      gap: '1.5rem'
    },
    leftColumn: {
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem'
    },
    card: {
      background: 'white',
      borderRadius: '0.75rem',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      overflow: 'hidden'
    },
    cardPadding: {
      padding: '1.5rem'
    },
    cardHeader: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: '1.5rem'
    },
    sectionTitle: {
      fontSize: '1.25rem',
      fontWeight: '600',
      color: '#1f2937'
    },
    navButtons: {
      display: 'flex',
      gap: '0.5rem'
    },
    navButton: {
      padding: '0.5rem',
      borderRadius: '0.5rem',
      border: '1px solid #d1d5db',
      background: 'white',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    disabledButton: {
      opacity: 0.5,
      cursor: 'not-allowed'
    },
    content: {
      color: '#374151',
      lineHeight: 1.6,
      fontSize: '16px'
    },
    sidebar: {
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem'
    },
    infoCard: {
      background: 'white',
      borderRadius: '0.75rem',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      padding: '1.5rem'
    },
    infoTitle: {
      fontSize: '1rem',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '0.75rem',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem'
    },
    infoText: {
      color: '#6b7280',
      fontSize: '0.875rem',
      marginBottom: '1rem'
    },
    sectionNav: {
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem'
    },
    sectionButton: {
      width: '100%',
      textAlign: 'left',
      padding: '0.75rem',
      borderRadius: '0.5rem',
      border: '1px solid #e5e7eb',
      background: '#f9fafb',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    activeSectionButton: {
      background: '#dbeafe',
      borderColor: '#bfdbfe',
      color: '#1d4ed8'
    },
    sectionButtonContent: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem'
    },
    sectionNumber: {
      width: '1.5rem',
      height: '1.5rem',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '0.75rem',
      fontWeight: '500',
      background: '#d1d5db',
      color: '#6b7280'
    },
    activeSectionNumber: {
      background: '#2563eb',
      color: 'white'
    },
    footer: {
      background: 'white',
      borderRadius: '0.75rem',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      padding: '1.5rem',
      marginTop: '2rem'
    },
    footerContent: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    },
    footerButtons: {
      display: 'flex',
      gap: '0.75rem'
    },
    primaryButton: {
      background: '#2563eb',
      color: 'white',
      padding: '0.5rem 1rem',
      borderRadius: '0.5rem',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      transition: 'all 0.2s ease'
    },
    secondaryButton: {
      background: '#f1f5f9',
      color: '#374151',
      padding: '0.5rem 1rem',
      borderRadius: '0.5rem',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      transition: 'all 0.2s ease'
    },
    progressDots: {
      display: 'flex',
      gap: '0.25rem'
    },
    progressDot: {
      width: '0.5rem',
      height: '0.5rem',
      borderRadius: '50%',
      background: '#d1d5db'
    },
    activeDot: {
      background: '#2563eb'
    },
    loadingScreen: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    },
    loadingCard: {
      background: 'white',
      borderRadius: '0.75rem',
      boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)',
      padding: '2rem',
      maxWidth: '400px',
      width: '100%',
      textAlign: 'center'
    },
    errorScreen: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #fecaca 0%, #fca5a5 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem'
    }
  };

  useEffect(() => {
    const fetchModuleData = async () => {
      setIsLoading(true);
      setError(null);
      setDebugInfo(null);
      
      try {
        console.log(`🔍 Fetching module data for course ${courseId}, module ${moduleIndex}`);
        
        const response = await fetch(`/api/courses/${courseId}`);
        console.log(`📡 API Response status: ${response.status}`);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: Error cargando el curso`);
        }
        
        const courseData = await response.json();
        console.log(`📊 Course data received:`, {
          courseName: courseData.metadata?.title,
          totalModules: courseData.modules?.length,
          requestedModule: moduleIndex
        });
        
        const module = courseData.modules[moduleIndex];
        
        if (!module || module === null) {
          console.log(`⚠️ Module ${moduleIndex + 1} not available, checking background generation...`);
          setIsGenerating(true);
          setDebugInfo(`Módulo ${moduleIndex + 1} siendo generado...`);
          
          let attempts = 0;
          const maxAttempts = 30;
          
          while (attempts < maxAttempts) {
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            console.log(`🔄 Retry attempt ${attempts + 1}/${maxAttempts}`);
            
            const retryResponse = await fetch(`/api/courses/${courseId}`);
            if (retryResponse.ok) {
              const retryData = await retryResponse.json();
              const retryModule = retryData.modules[moduleIndex];
              
              if (retryModule && retryModule !== null) {
                console.log(`✅ Module ${moduleIndex + 1} now available!`);
                setModuleData(retryModule);
                setIsGenerating(false);
                setIsLoading(false);
                setCurrentChunk(0);
                setDebugInfo(null);
                return;
              }
            }
            
            attempts++;
            setDebugInfo(`Esperando módulo ${moduleIndex + 1}... intento ${attempts}/${maxAttempts}`);
          }
          
          if (attempts >= maxAttempts) {
            console.log(`🔧 Module ${moduleIndex + 1} not available after waiting, trying on-demand generation...`);
            try {
              setDebugInfo('Generando módulo bajo demanda...');
              const generateResponse = await fetch(`/api/courses/${courseId}/generate-module/${moduleIndex}`, {
                method: 'POST'
              });
              
              if (!generateResponse.ok) {
                throw new Error('Error generando el módulo bajo demanda');
              }
              
              const generateData = await generateResponse.json();
              setModuleData(generateData.module);
              setIsGenerating(false);
              setIsLoading(false);
              setCurrentChunk(0);
              setDebugInfo(null);
            } catch (generateError) {
              console.error('Error en generación bajo demanda:', generateError);
              setError(`El módulo ${moduleIndex + 1} aún se está generando. Por favor intenta en unos momentos.`);
              setIsLoading(false);
              setIsGenerating(false);
            }
          }
        } else {
          console.log(`✅ Module ${moduleIndex + 1} loaded successfully`);
          setModuleData(module);
          setIsLoading(false);
          setCurrentChunk(0);
          setDebugInfo(null);
        }
      } catch (err) {
        console.error('❌ Error fetching module data:', err);
        setError(err.message);
        setDebugInfo(`Error: ${err.message}`);
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
      <div style={styles.loadingScreen}>
        <div style={styles.loadingCard}>
          <div className="loading-spinner" style={{ margin: '0 auto 1rem', width: '48px', height: '48px' }}></div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem' }}>
            {isGenerating 
              ? `🚀 Generando Módulo ${moduleIndex + 1}...` 
              : 'Cargando módulo...'
            }
          </h3>
          {isGenerating && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                ⚡ Creando contenido personalizado con IA
              </p>
              <div style={{ background: '#dbeafe', border: '1px solid #bfdbfe', borderRadius: '0.5rem', padding: '0.75rem' }}>
                <p style={{ fontSize: '0.75rem', color: '#1d4ed8' }}>
                  💡 <strong>Tip:</strong> Los próximos módulos se cargarán instantáneamente
                </p>
              </div>
            </div>
          )}
          {debugInfo && (
            <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#f1f5f9', borderRadius: '0.5rem' }}>
              <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Debug: {debugInfo}</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.errorScreen}>
        <div style={styles.loadingCard}>
          <div style={{ color: '#ef4444', marginBottom: '1rem' }}>
            <AlertCircle size={64} style={{ margin: '0 auto' }} />
          </div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937', marginBottom: '0.5rem' }}>Error</h3>
          <p style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</p>
          {debugInfo && (
            <div style={{ marginBottom: '1rem', padding: '0.75rem', background: '#f1f5f9', borderRadius: '0.5rem' }}>
              <p style={{ fontSize: '0.75rem', color: '#6b7280' }}>Debug: {debugInfo}</p>
            </div>
          )}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <button 
              onClick={onBack} 
              style={{ ...styles.primaryButton, width: '100%' }}
            >
              <ArrowLeft size={16} />
              Volver al Curso
            </button>
            <button 
              onClick={() => window.location.reload()} 
              style={{ ...styles.secondaryButton, width: '100%' }}
            >
              🔄 Recargar Página
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!moduleData) {
    return (
      <div style={{ ...styles.loadingScreen, background: 'linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%)' }}>
        <div style={styles.loadingCard}>
          <p style={{ color: '#6b7280' }}>No hay datos del módulo disponibles</p>
          <button 
            onClick={onBack} 
            style={{ ...styles.primaryButton, marginTop: '1rem' }}
          >
            Volver al Curso
          </button>
        </div>
      </div>
    );
  }

  const currentChunkData = moduleData.chunks[currentChunk];
  const progress = ((currentChunk + 1) / moduleData.chunks.length) * 100;

  const getCurrentVideo = () => {
    try {
      if (currentChunkData?.video) {
        return currentChunkData.video;
      }
      
      if (moduleData.resources?.videos && moduleData.resources.videos.length > 0) {
        return moduleData.resources.videos[0];
      }
      
      return null;
    } catch (error) {
      console.error('Error getting current video:', error);
      return null;
    }
  };

  const currentVideo = getCurrentVideo();

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.headerContent}>
          <div style={styles.headerLeft}>
            <button 
              onClick={onBack}
              style={styles.backButton}
              onMouseOver={(e) => e.target.style.background = '#e2e8f0'}
              onMouseOut={(e) => e.target.style.background = '#f1f5f9'}
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <h1 style={styles.title}>
                {moduleData.title || `Módulo ${moduleIndex + 1}`}
              </h1>
              <p style={styles.subtitle}>
                Módulo {moduleIndex + 1} de {totalModules}
              </p>
            </div>
          </div>
          
          <div style={styles.progressContainer}>
            <div style={styles.progressText}>
              Sección {currentChunk + 1} de {moduleData.chunks?.length || 0}
            </div>
            <div style={styles.progressBar}>
              <div 
                style={{ ...styles.progressFill, width: `${progress}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div style={styles.mainContent}>
        {/* Main Content Area */}
        <div style={styles.leftColumn}>
          
          {/* Video Section */}
          {currentVideo && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              style={styles.card}
            >
              <div style={styles.cardPadding}>
                <h3 style={{ ...styles.infoTitle, marginBottom: '1rem' }}>
                  <Video size={20} style={{ color: '#dc2626' }} />
                  Video de la Sección
                </h3>
                <YouTubePlayer video={currentVideo} />
              </div>
            </motion.div>
          )}

          {/* Content Section */}
          <motion.div
            key={currentChunk}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            style={styles.card}
          >
            <div style={styles.cardPadding}>
              <div style={styles.cardHeader}>
                <h2 style={styles.sectionTitle}>
                  Contenido: Sección {currentChunk + 1}
                </h2>
                <div style={styles.navButtons}>
                  <button
                    onClick={prevChunk}
                    disabled={currentChunk === 0}
                    style={{
                      ...styles.navButton,
                      ...(currentChunk === 0 ? styles.disabledButton : {})
                    }}
                    onMouseOver={(e) => !e.target.disabled && (e.target.style.background = '#f9fafb')}
                    onMouseOut={(e) => !e.target.disabled && (e.target.style.background = 'white')}
                  >
                    <ChevronLeft size={20} />
                  </button>
                  <button
                    onClick={nextChunk}
                    disabled={currentChunk === (moduleData.chunks?.length || 1) - 1}
                    style={{
                      ...styles.navButton,
                      ...(currentChunk === (moduleData.chunks?.length || 1) - 1 ? styles.disabledButton : {})
                    }}
                    onMouseOver={(e) => !e.target.disabled && (e.target.style.background = '#f9fafb')}
                    onMouseOut={(e) => !e.target.disabled && (e.target.style.background = 'white')}
                  >
                    <ChevronRight size={20} />
                  </button>
                </div>
              </div>

              <div 
                style={styles.content}
                dangerouslySetInnerHTML={{ __html: currentChunkData?.content || 'Contenido no disponible' }}
              />
            </div>
          </motion.div>
        </div>

        {/* Sidebar */}
        <div style={styles.sidebar}>
          {/* Module Info */}
          <div style={styles.infoCard}>
            <h3 style={styles.infoTitle}>
              <BookOpen size={20} style={{ color: '#2563eb' }} />
              Información del Módulo
            </h3>
            <p style={styles.infoText}>
              {moduleData.description || 'Descripción no disponible'}
            </p>
            
            {moduleData.objective && (
              <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '1rem' }}>
                <h4 style={{ ...styles.infoTitle, fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                  <Target size={16} style={{ color: '#10b981' }} />
                  Objetivo
                </h4>
                <p style={styles.infoText}>
                  {moduleData.objective}
                </p>
              </div>
            )}
          </div>

          {/* Section Navigation */}
          <div style={styles.infoCard}>
            <h3 style={styles.infoTitle}>Secciones</h3>
            <div style={styles.sectionNav}>
              {(moduleData.chunks || []).map((chunk, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentChunk(index)}
                  style={{
                    ...styles.sectionButton,
                    ...(index === currentChunk ? styles.activeSectionButton : {})
                  }}
                  onMouseOver={(e) => index !== currentChunk && (e.target.style.background = '#f3f4f6')}
                  onMouseOut={(e) => index !== currentChunk && (e.target.style.background = '#f9fafb')}
                >
                  <div style={styles.sectionButtonContent}>
                    <div style={{
                      ...styles.sectionNumber,
                      ...(index === currentChunk ? styles.activeSectionNumber : {})
                    }}>
                      {index + 1}
                    </div>
                    <span style={{ fontSize: '0.875rem' }}>
                      {(moduleData.concepts && moduleData.concepts[index]) || `Sección ${index + 1}`}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Footer */}
      <div style={styles.footer}>
        <div style={styles.footerContent}>
          <div style={styles.footerButtons}>
            {onPrevModule && (
              <button 
                onClick={onPrevModule} 
                style={styles.secondaryButton}
                onMouseOver={(e) => e.target.style.background = '#e2e8f0'}
                onMouseOut={(e) => e.target.style.background = '#f1f5f9'}
              >
                <ArrowLeft size={16} />
                Módulo Anterior
              </button>
            )}
          </div>

          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.25rem' }}>
              Progreso del módulo
            </div>
            <div style={styles.progressDots}>
              {(moduleData.chunks || []).map((_, index) => (
                <div
                  key={index}
                  style={{
                    ...styles.progressDot,
                    ...(index <= currentChunk ? styles.activeDot : {})
                  }}
                />
              ))}
            </div>
          </div>

          <div style={styles.footerButtons}>
            {onNextModule ? (
              <button 
                onClick={onNextModule} 
                style={styles.primaryButton}
                onMouseOver={(e) => e.target.style.background = '#1d4ed8'}
                onMouseOut={(e) => e.target.style.background = '#2563eb'}
              >
                Módulo Siguiente
                <ArrowRight size={16} />
              </button>
            ) : (
              <button 
                onClick={onBack} 
                style={{ ...styles.primaryButton, background: '#10b981' }}
                onMouseOver={(e) => e.target.style.background = '#059669'}
                onMouseOut={(e) => e.target.style.background = '#10b981'}
              >
                <CheckCircle size={16} />
                Completar Curso
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModuleViewer; 