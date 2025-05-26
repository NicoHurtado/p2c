import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FiBook, FiClock, FiUser, FiTarget, FiArrowLeft, FiTrash2, FiChevronDown, FiChevronUp, FiPlay } from 'react-icons/fi';
import Layout from '../components/Layout';
import { courseService } from '../services/api';
import { ThemeContext } from '../context/ThemeContext';
import ImmersiveCourseView from '../components/ImmersiveCourseView';

const CourseView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { darkMode } = useContext(ThemeContext);
  
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedModule, setExpandedModule] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [immersiveMode, setImmersiveMode] = useState(false);

  useEffect(() => {
    fetchCourse();
  }, [id]);

  const fetchCourse = async () => {
    try {
      setLoading(true);
      const courseData = await courseService.getCourse(id);
      setCourse(courseData);
    } catch (error) {
      console.error('Error fetching course:', error);
      setError('Error al cargar el curso');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este curso?')) {
      try {
        await courseService.deleteCourse(id);
        navigate('/dashboard');
      } catch (error) {
        console.error('Error deleting course:', error);
        setError('Error al eliminar el curso');
      }
    }
  };

  const toggleModule = (index) => {
    setExpandedModule(expandedModule === index ? null : index);
  };

  const startImmersiveMode = () => {
    setImmersiveMode(true);
  };

  const exitImmersiveMode = () => {
    setImmersiveMode(false);
  };

  const renderMarkdown = (content) => {
    if (!content) return null;
    
    // Simple markdown rendering for basic formatting
    return content
      .split('\n')
      .map((line, index) => {
        if (line.startsWith('### ')) {
          return <h3 key={index} className="text-lg font-semibold mt-4 mb-2 text-gray-800 dark:text-white">{line.replace('### ', '')}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={index} className="text-xl font-bold mt-6 mb-3 text-gray-900 dark:text-white">{line.replace('## ', '')}</h2>;
        }
        if (line.startsWith('# ')) {
          return <h1 key={index} className="text-2xl font-bold mt-8 mb-4 text-gray-900 dark:text-white">{line.replace('# ', '')}</h1>;
        }
        if (line.startsWith('- ') || line.startsWith('* ')) {
          return <li key={index} className="ml-4 text-gray-700 dark:text-gray-300">{line.replace(/^[*-] /, '')}</li>;
        }
        if (line.startsWith('**') && line.endsWith('**')) {
          return <p key={index} className="font-semibold text-gray-800 dark:text-white mt-2">{line.replace(/\*\*/g, '')}</p>;
        }
        if (line.trim() === '') {
          return <br key={index} />;
        }
        return <p key={index} className="text-gray-700 dark:text-gray-300 mt-1">{line}</p>;
      });
  };

  const tabs = [
    { id: 'overview', label: 'Resumen', icon: FiTarget },
    { id: 'modules', label: 'Módulos', icon: FiBook },
    { id: 'roadmap', label: 'Mapa de Aprendizaje', icon: FiClock },
    { id: 'assistant', label: 'Asistente Virtual', icon: FiUser },
  ];

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-700 dark:text-red-400">{error}</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!course) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">Curso no encontrado</p>
          </div>
        </div>
      </Layout>
    );
  }

  const courseContent = course.content || {};

  return (
    <>
      <AnimatePresence>
        {immersiveMode && (
          <ImmersiveCourseView course={course} onClose={exitImmersiveMode} />
        )}
      </AnimatePresence>
      
      {!immersiveMode && (
        <Layout>
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-6">
              <button
                onClick={() => navigate('/dashboard')}
                className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 mb-4"
              >
                <FiArrowLeft size={16} />
                Volver al Dashboard
              </button>
              
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {courseContent.titulo || course.title}
                  </h1>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">
                    {courseContent.descripcion || 'Curso personalizado'}
                  </p>
                  <div className="flex flex-wrap gap-4 text-sm">
                    <span className="flex items-center gap-1 px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
                      <FiTarget size={14} />
                      {courseContent.nivel || course.experience_level}
                    </span>
                    <span className="flex items-center gap-1 px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full">
                      <FiClock size={14} />
                      {courseContent.duracion || course.available_time}
                    </span>
                    <span className="flex items-center gap-1 px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded-full">
                      <FiBook size={14} />
                      {courseContent.modulos?.length || 0} módulos
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={startImmersiveMode}
                    className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                  >
                    <FiPlay size={16} />
                    Empezar Curso
                  </button>
                  <button
                    onClick={handleDelete}
                    className="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                  >
                    <FiTrash2 size={16} />
                    Eliminar
                  </button>
                </div>
              </div>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
              <nav className="flex space-x-8">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                        activeTab === tab.id
                          ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                          : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                      }`}
                    >
                      <Icon size={16} />
                      {tab.label}
                    </button>
                  );
                })}
              </nav>
            </div>

            {/* Content */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  {courseContent.conocimientos_previos && (
                    <div>
                      <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                        Conocimientos Previos
                      </h3>
                      <div className="prose dark:prose-invert max-w-none">
                        {renderMarkdown(courseContent.conocimientos_previos)}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'modules' && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                    Módulos del Curso ({courseContent.modulos?.length || 0})
                  </h3>
                  {courseContent.modulos?.map((modulo, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
                    >
                      <button
                        onClick={() => toggleModule(index)}
                        className="w-full px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 flex items-center justify-between transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          <span className="flex items-center justify-center w-8 h-8 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 rounded-full text-sm font-semibold">
                            {index + 1}
                          </span>
                          <div className="text-left">
                            <h4 className="font-semibold text-gray-900 dark:text-white">
                              {modulo.titulo}
                            </h4>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {modulo.descripcion}
                            </p>
                          </div>
                        </div>
                        {expandedModule === index ? (
                          <FiChevronUp className="text-gray-500" />
                        ) : (
                          <FiChevronDown className="text-gray-500" />
                        )}
                      </button>
                      
                      {expandedModule === index && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="px-4 py-4 border-t border-gray-200 dark:border-gray-700"
                        >
                          <div className="space-y-4">
                            {modulo.contenido && (
                              <div>
                                <h5 className="font-semibold text-gray-900 dark:text-white mb-2">
                                  Contenido
                                </h5>
                                <div className="prose dark:prose-invert max-w-none text-sm">
                                  {renderMarkdown(modulo.contenido)}
                                </div>
                              </div>
                            )}
                            
                            {modulo.recursos && (
                              <div>
                                <h5 className="font-semibold text-gray-900 dark:text-white mb-2">
                                  Recursos
                                </h5>
                                <div className="prose dark:prose-invert max-w-none text-sm">
                                  {renderMarkdown(modulo.recursos)}
                                </div>
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'roadmap' && (
                <div>
                  <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                    Mapa de Aprendizaje
                  </h3>
                  <div className="prose dark:prose-invert max-w-none">
                    {renderMarkdown(courseContent.mapa_aprendizaje)}
                  </div>
                </div>
              )}

              {activeTab === 'assistant' && (
                <div>
                  <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                    Tu Asistente Virtual
                  </h3>
                  <div className="prose dark:prose-invert max-w-none">
                    {renderMarkdown(courseContent.asistente_virtual)}
                  </div>
                </div>
              )}
            </div>
          </div>
        </Layout>
      )}
    </>
  );
};

export default CourseView; 