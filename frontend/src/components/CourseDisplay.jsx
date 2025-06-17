import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Clock, 
  Target, 
  CheckCircle, 
  PlayCircle, 
  Download,
  RefreshCw,
  Star,
  Users,
  Trophy,
  Podcast,
  Volume2
} from 'lucide-react';

const CourseDisplay = ({ courseData, onStartNew, onModuleStart }) => {
  const [podcastAudioUrl, setPodcastAudioUrl] = useState(null);
  
  // Debug logging
  console.log('🎯 CourseDisplay received courseData:', courseData);
  
  // Destructure from courseData structure returned by backend
  const { course_id, metadata, modules_metadata, status, generation_started, estimated_completion_time } = courseData || {};
  const { title, description, level, total_modules, module_list, topics, podcast_audio_url, podcast_script } = metadata || {};
  
  console.log('🎯 Extracted data:', { course_id, title, total_modules, status });
  console.log('🎯 Modules metadata received:', modules_metadata);
  console.log('🎯 Generation started:', generation_started);
  console.log('🎯 Estimated completion:', estimated_completion_time);
  console.log('🎧 PODCAST DEBUG - audio_url:', podcast_audio_url);
  console.log('🎧 PODCAST DEBUG - script:', podcast_script);
  console.log('🎧 PODCAST DEBUG - metadata completa:', metadata);
  
  // Verificar periódicamente si el audio del podcast está disponible
  useEffect(() => {
    // Si ya tenemos el audio, configurarlo
    if (podcast_audio_url) {
      setPodcastAudioUrl(podcast_audio_url);
      return;
    }
    
    // Si no tenemos el audio pero tenemos course_id, verificar periódicamente
    if (course_id && !podcast_audio_url) {
      const checkPodcastAudio = async () => {
        try {
          const response = await fetch(`/api/courses/${course_id}`);
          if (response.ok) {
            const courseData = await response.json();
            console.log('🎧 CHECKING for podcast audio:', courseData.metadata?.podcast_audio_url);
            
            if (courseData.metadata?.podcast_audio_url) {
              setPodcastAudioUrl(courseData.metadata.podcast_audio_url);
              console.log('✅ Podcast audio found:', courseData.metadata.podcast_audio_url);
            }
          }
        } catch (error) {
          console.error('Error checking podcast audio:', error);
        }
      };
      
      // Verificar inmediatamente
      checkPodcastAudio();
      
      // Verificar cada 5 segundos hasta encontrar el audio
      const interval = setInterval(() => {
        if (!podcastAudioUrl) {
          checkPodcastAudio();
        } else {
          clearInterval(interval);
        }
      }, 5000);
      
      // Limpiar intervalo después de 2 minutos
      setTimeout(() => {
        clearInterval(interval);
      }, 120000);
      
      return () => clearInterval(interval);
    }
  }, [course_id, podcast_audio_url, podcastAudioUrl]);

  // Safety check - if no courseData, show loading state
  if (!courseData) {
    console.log('🎯 No courseData - showing loading state');
    return (
      <div className="course-display">
        <div className="container text-center" style={{ padding: '3rem' }}>
          <p className="text-gray-600">Cargando datos del curso...</p>
        </div>
      </div>
    );
  }

  // Additional safety checks
  if (!metadata) {
    console.log('🎯 No metadata - showing error state');
    return (
      <div className="course-display">
        <div className="container text-center" style={{ padding: '3rem' }}>
          <p className="text-red-600">Error: No se pudieron cargar los metadatos del curso</p>
          <button onClick={onStartNew} className="btn btn-secondary" style={{ marginTop: '1rem' }}>
            Crear Nuevo Curso
          </button>
        </div>
      </div>
    );
  }

  if (!title) {
    console.log('🎯 No title - showing error state');
    return (
      <div className="course-display">
        <div className="container text-center" style={{ padding: '3rem' }}>
          <p className="text-red-600">Error: No se pudo generar el título del curso</p>
          <button onClick={onStartNew} className="btn btn-secondary" style={{ marginTop: '1rem' }}>
            Crear Nuevo Curso
          </button>
        </div>
      </div>
    );
  }

  console.log('🎯 All validations passed - rendering course display');

  const levelConfig = {
    principiante: { label: "Principiante", color: "#10b981", icon: "🌱" },
    intermedio: { label: "Intermedio", color: "#f59e0b", icon: "🚀" },
    avanzado: { label: "Avanzado", color: "#ef4444", icon: "⭐" }
  };

  const currentLevelConfig = levelConfig[level] || levelConfig.principiante;

  const handleStartCourse = async () => {
    // Start the first module immediately
    if (onModuleStart) {
      onModuleStart(0);
    }
  };

  const handlePlayPodcast = (audioUrl) => {
    try {
      // Crear un elemento de audio y reproducirlo
      const audio = new Audio(audioUrl);
      audio.play().catch(error => {
        console.error('Error reproduciendo el podcast:', error);
        alert('No se pudo reproducir el audio. Por favor, verifica que el archivo esté disponible.');
      });
    } catch (error) {
      console.error('Error creando el reproductor de audio:', error);
      alert('Error al crear el reproductor de audio.');
    }
  };

  return (
    <div className="course-display">
      {/* Hero Section */}
      <div className="course-header">
        <div className="container">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div style={{ marginBottom: '1rem' }}>
              <span style={{
                background: 'rgba(255, 255, 255, 0.2)',
                padding: '0.5rem 1rem',
                borderRadius: '20px',
                fontSize: '0.875rem',
                fontWeight: '500',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                <Trophy size={16} />
                Curso Generado con Éxito
              </span>
            </div>
            
            <h1 className="text-4xl font-bold mb-4">
              {title || "Curso Personalizado"}
            </h1>
            
            <p className="text-lg mb-6" style={{ opacity: 0.9 }}>
              {description || "Descripción del curso se está generando..."}
            </p>
            
            <div style={{
              display: 'flex',
              gap: '2rem',
              alignItems: 'center',
              flexWrap: 'wrap',
              justifyContent: 'center'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <BookOpen size={20} />
                <span>{total_modules || 0} módulos</span>
              </div>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Target size={20} />
                <span>{currentLevelConfig.icon} {currentLevelConfig.label}</span>
              </div>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Clock size={20} />
                <span>~{(total_modules || 0) * 2}h estimadas</span>
              </div>
            </div>
            
            {/* Botón del Podcast */}
            {podcastAudioUrl && (
              <div style={{ marginTop: '2rem' }}>
                <motion.button
                  onClick={() => handlePlayPodcast(podcastAudioUrl)}
                  style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '25px',
                    padding: '0.75rem 1.5rem',
                    fontSize: '1rem',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    cursor: 'pointer',
                    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
                    transition: 'all 0.3s ease'
                  }}
                  whileHover={{ 
                    scale: 1.05,
                    boxShadow: '0 6px 20px rgba(102, 126, 234, 0.6)'
                  }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Podcast size={20} />
                  🎧 Escuchar Introducción
                </motion.button>
              </div>
            )}
            
            {/* Botón de debug temporal */}
            {!podcastAudioUrl && (
              <div style={{ marginTop: '2rem' }}>
                <div style={{
                  background: '#f59e0b',
                  color: 'white',
                  padding: '0.5rem 1rem',
                  borderRadius: '8px',
                  fontSize: '0.875rem'
                }}>
                  🔍 Debug: Audio del podcast no disponible aún
                  {podcast_script && <div>✅ Script generado</div>}
                  {!podcast_script && <div>❌ Script no encontrado</div>}
                  <div>🔄 Verificando cada 5 segundos...</div>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>

      {/* Course Content */}
      <div className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
        {/* Topics */}
        {topics && topics.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-8"
          >
            <div className="card">
              <div className="card-header">
                <h3 className="text-xl font-semibold" style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '0.5rem',
                  margin: 0
                }}>
                  <Star size={24} style={{ color: '#f59e0b' }} />
                  Temas Principales
                </h3>
              </div>
              <div className="card-body">
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                  gap: '1rem'
                }}>
                  {topics && topics.length > 0 ? topics.map((topic, index) => (
                    <div
                      key={index}
                      style={{
                        padding: '1rem',
                        background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
                        borderRadius: '8px',
                        border: '1px solid #e2e8f0',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.75rem'
                      }}
                    >
                      <div style={{
                        background: '#4f46e5',
                        color: 'white',
                        borderRadius: '50%',
                        width: '24px',
                        height: '24px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '0.75rem',
                        fontWeight: '600'
                      }}>
                        {index + 1}
                      </div>
                      <span className="font-medium">{topic}</span>
                    </div>
                  )) : (
                    <p className="text-gray-600 text-center">
                      Los temas se están procesando...
                    </p>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Modules */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div style={{ marginBottom: '2rem' }}>
            <h3 className="text-2xl font-bold mb-2" style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <BookOpen size={28} style={{ color: '#4f46e5' }} />
              Módulos del Curso
            </h3>
            <p className="text-gray-600">
              Contenido estructurado para maximizar tu aprendizaje
            </p>
          </div>

          <div className="course-modules">
            {modules_metadata && modules_metadata.length > 0 ? modules_metadata.map((moduleData, index) => (
              <motion.div
                key={`module-${index}`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.1 * index }}
                className="module-card"
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                  <div className="module-number">
                    {index + 1}
                  </div>
                  
                  <div style={{ flex: 1 }}>
                    <h4 className="text-xl font-semibold mb-3" style={{ color: '#1f2937' }}>
                      {moduleData.title}
                    </h4>
                    
                    <p className="text-gray-600 mb-3" style={{ lineHeight: 1.6 }}>
                      {moduleData.description}
                    </p>

                    <div style={{
                      background: '#f8fafc',
                      padding: '0.75rem',
                      borderRadius: '6px',
                      border: '1px solid #e2e8f0',
                      marginBottom: '1rem'
                    }}>
                      <p style={{ 
                        fontSize: '0.875rem', 
                        fontWeight: '500',
                        color: '#374151',
                        margin: 0
                      }}>
                        🎯 <strong>Objetivo:</strong> {moduleData.objective}
                      </p>
                    </div>
                    
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      paddingTop: '1rem',
                      borderTop: '1px solid #e5e7eb'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <span style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.25rem',
                          fontSize: '0.875rem',
                          color: '#6b7280'
                        }}>
                          <Clock size={14} />
                          ~{moduleData.estimated_duration}h
                        </span>
                        
                        <span style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.25rem',
                          fontSize: '0.875rem',
                          color: '#6b7280'
                        }}>
                          <BookOpen size={14} />
                          {moduleData.total_concepts} conceptos
                        </span>
                      </div>
                      
                      <button 
                        onClick={() => onModuleStart && onModuleStart(index)}
                        className="btn btn-secondary" 
                        style={{ fontSize: '0.875rem' }}
                      >
                        <PlayCircle size={16} />
                        Acceder al Módulo
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            )) : (
              <div className="text-center" style={{ padding: '3rem' }}>
                <p className="text-gray-600">
                  Los metadatos del curso se están procesando... Por favor espera un momento.
                </p>
              </div>
            )}
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          style={{
            display: 'flex',
            gap: '1rem',
            justifyContent: 'center',
            marginTop: '3rem',
            flexWrap: 'wrap'
          }}
        >
          <button 
            onClick={handleStartCourse}
            className="btn btn-primary btn-lg"
          >
            <CheckCircle size={20} />
            Comenzar Curso
          </button>
          
          <button className="btn btn-secondary btn-lg">
            <Download size={20} />
            Descargar PDF
          </button>
          
          <button 
            onClick={onStartNew}
            className="btn btn-secondary btn-lg"
          >
            <RefreshCw size={20} />
            Crear Otro Curso
          </button>
        </motion.div>

        {/* Course Info Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          style={{ marginTop: '3rem' }}
        >
          <div className="card" style={{
            background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
            color: 'white',
            border: 'none'
          }}>
            <div className="card-body text-center">
              <h4 className="text-lg font-semibold mb-2">
                🎉 ¡Tu curso está listo!
              </h4>
              <p style={{ opacity: 0.9, margin: 0 }}>
                <strong>ID del curso:</strong> {course_id}
              </p>
              <p style={{ opacity: 0.8, fontSize: '0.875rem', marginTop: '0.5rem', margin: 0 }}>
                Guarda este ID para acceder a tu curso más tarde
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default CourseDisplay; 