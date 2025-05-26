import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FiBook, FiClock, FiUser, FiTarget, FiCheckCircle, FiChevronDown, FiChevronUp, FiSave } from 'react-icons/fi';

const CourseDisplay = ({ course, onSave, onClose, darkMode }) => {
  const [expandedModule, setExpandedModule] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  const toggleModule = (index) => {
    setExpandedModule(expandedModule === index ? null : index);
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

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 overflow-y-auto"
    >
      <div className="min-h-screen py-8 px-4">
        <div className="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-2xl">
          {/* Header */}
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  {course.titulo}
                </h1>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  {course.descripcion}
                </p>
                <div className="flex flex-wrap gap-4 text-sm">
                  <span className="flex items-center gap-1 px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
                    <FiTarget size={14} />
                    {course.nivel}
                  </span>
                  <span className="flex items-center gap-1 px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full">
                    <FiClock size={14} />
                    {course.duracion}
                  </span>
                  <span className="flex items-center gap-1 px-3 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded-full">
                    <FiBook size={14} />
                    {course.modulos?.length || 0} módulos
                  </span>
                </div>
              </div>
              <div className="flex gap-2 ml-4">
                <button
                  onClick={onSave}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  <FiSave size={16} />
                  Guardar Curso
                </button>
                <button
                  onClick={onClose}
                  className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="flex space-x-8 px-6">
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
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {course.conocimientos_previos && (
                  <div>
                    <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">
                      Conocimientos Previos
                    </h3>
                    <div className="prose dark:prose-invert max-w-none">
                      {renderMarkdown(course.conocimientos_previos)}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'modules' && (
              <div className="space-y-4">
                <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                  Módulos del Curso ({course.modulos?.length || 0})
                </h3>
                {course.modulos?.map((modulo, index) => (
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
                  {renderMarkdown(course.mapa_aprendizaje)}
                </div>
              </div>
            )}

            {activeTab === 'assistant' && (
              <div>
                <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                  Tu Asistente Virtual
                </h3>
                <div className="prose dark:prose-invert max-w-none">
                  {renderMarkdown(course.asistente_virtual)}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default CourseDisplay; 