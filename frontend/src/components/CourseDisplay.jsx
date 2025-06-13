import React from 'react';
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
  Trophy
} from 'lucide-react';

const CourseDisplay = ({ courseData, onStartNew, onModuleStart }) => {
  // Destructure from courseData structure returned by backend
  const { course_id, metadata, status } = courseData;
  const { title, description, level, total_modules, module_list, topics } = metadata || {};

  const levelConfig = {
    principiante: { label: "Principiante", color: "#10b981", icon: "🌱" },
    intermedio: { label: "Intermedio", color: "#f59e0b", icon: "🚀" },
    avanzado: { label: "Avanzado", color: "#ef4444", icon: "⭐" }
  };

  const currentLevelConfig = levelConfig[level] || levelConfig.principiante;

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
            {module_list && module_list.length > 0 ? module_list.map((moduleTitle, index) => (
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
                      {moduleTitle}
                    </h4>
                    
                    <p className="text-gray-600 mb-4" style={{ lineHeight: 1.6 }}>
                      {index === 0 ? 
                        'Módulo inicial con fundamentos y conceptos básicos. ¡Ya está listo para comenzar!' :
                        'Este módulo se generará automáticamente cuando hagas click para acceder.'
                      }
                    </p>
                    
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
                          ~2h
                        </span>
                        
                        <span style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.25rem',
                          fontSize: '0.875rem',
                          color: '#6b7280'
                        }}>
                          <Users size={14} />
                          {Math.floor(Math.random() * 1000) + 500}+ estudiantes
                        </span>

                        {index === 0 && (
                          <span style={{
                            padding: '0.25rem 0.5rem',
                            background: '#10b981',
                            color: 'white',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                            fontWeight: '600'
                          }}>
                            ✓ Listo
                          </span>
                        )}

                        {index > 0 && (
                          <span style={{
                            padding: '0.25rem 0.5rem',
                            background: '#f59e0b',
                            color: 'white',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                            fontWeight: '600'
                          }}>
                            🤖 Generación IA
                          </span>
                        )}
                      </div>
                      
                      <button 
                        onClick={() => onModuleStart && onModuleStart(index)}
                        className="btn btn-secondary" 
                        style={{ fontSize: '0.875rem' }}
                      >
                        <PlayCircle size={16} />
                        {index === 0 ? 'Empezar Módulo' : 'Generar y Empezar'}
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
            onClick={() => onModuleStart && onModuleStart(0)}
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