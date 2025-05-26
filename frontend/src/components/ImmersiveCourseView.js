import React, { useState, useEffect, useContext } from 'react';
import { FiX, FiArrowLeft, FiArrowRight, FiExternalLink } from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';
import { ThemeContext } from '../context/ThemeContext';
import axios from 'axios';

const ImmersiveCourseView = ({ course, onClose }) => {
  const { darkMode } = useContext(ThemeContext);
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [currentView, setCurrentView] = useState('content'); // 'content' or 'resources'
  const [videoDetails, setVideoDetails] = useState({});
  const [loading, setLoading] = useState(false);
  
  const modules = course?.content?.modulos || [];
  const currentModule = modules[currentModuleIndex] || {};
  const youtubeApiKey = process.env.REACT_APP_YOUTUBE_API_KEY;
  
  useEffect(() => {
    if (currentView === 'resources' && currentModule.recursos) {
      extractAndFetchYouTubeVideos(currentModule.recursos);
    }
  }, [currentView, currentModuleIndex, currentModule.recursos]);
  
  const extractAndFetchYouTubeVideos = async (resources) => {
    if (!resources || !youtubeApiKey) return;
    
    setLoading(true);
    const lines = resources.split('\n');
    const videoIds = [];
    
    lines.forEach(line => {
      // Match YouTube links in the format: [title](https://www.youtube.com/watch?v=VIDEO_ID)
      const youtubeMatch = line.match(/\[([^\]]+)\]\((https?:\/\/(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+))\)/);
      
      // Match YouTube iframe embeds
      const iframeMatch = line.match(/src=(['"])https?:\/\/(www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)\1/);
      
      if (youtubeMatch) {
        const [, , , , videoId] = youtubeMatch;
        videoIds.push(videoId);
      } else if (iframeMatch) {
        const videoId = iframeMatch[3];
        videoIds.push(videoId);
      }
    });
    
    if (videoIds.length > 0) {
      try {
        const response = await axios.get(`https://www.googleapis.com/youtube/v3/videos`, {
          params: {
            part: 'snippet,contentDetails',
            id: videoIds.join(','),
            key: youtubeApiKey
          }
        });
        
        const videoDetailsMap = {};
        response.data.items.forEach(item => {
          videoDetailsMap[item.id] = {
            title: item.snippet.title,
            description: item.snippet.description,
            thumbnail: item.snippet.thumbnails.high.url,
            duration: item.contentDetails.duration
          };
        });
        
        setVideoDetails(videoDetailsMap);
      } catch (error) {
        console.error('Error fetching YouTube video details:', error);
      }
    }
    
    setLoading(false);
  };
  
  const goToNextModule = () => {
    if (currentModuleIndex < modules.length - 1) {
      setCurrentModuleIndex(currentModuleIndex + 1);
      setCurrentView('content');
      window.scrollTo(0, 0);
    }
  };
  
  const goToPreviousModule = () => {
    if (currentModuleIndex > 0) {
      setCurrentModuleIndex(currentModuleIndex - 1);
      setCurrentView('content');
      window.scrollTo(0, 0);
    }
  };

  // Función para crear markup seguro
  const createMarkup = (htmlContent) => {
    return { __html: htmlContent };
  };
  
  const renderMarkdown = (content) => {
    if (!content) return null;
    
    return content
      .split('\n')
      .map((line, index) => {
        // Check if line contains an iframe (YouTube embed)
        if (line.includes('<iframe') && line.includes('youtube.com/embed')) {
          return (
            <div key={index} className="my-6" dangerouslySetInnerHTML={createMarkup(line)} />
          );
        }
        
        if (line.startsWith('### ')) {
          return <h3 key={index} className="text-xl font-semibold mt-6 mb-3 text-gray-800 dark:text-white">{line.replace('### ', '')}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={index} className="text-2xl font-bold mt-8 mb-4 text-gray-900 dark:text-white">{line.replace('## ', '')}</h2>;
        }
        if (line.startsWith('# ')) {
          return <h1 key={index} className="text-3xl font-bold mt-10 mb-5 text-gray-900 dark:text-white">{line.replace('# ', '')}</h1>;
        }
        if (line.startsWith('- ') || line.startsWith('* ')) {
          return <li key={index} className="ml-6 text-gray-700 dark:text-gray-300 my-2">{line.replace(/^[*-] /, '')}</li>;
        }
        if (line.startsWith('**') && line.endsWith('**')) {
          return <p key={index} className="font-semibold text-gray-800 dark:text-white mt-3">{line.replace(/\*\*/g, '')}</p>;
        }
        if (line.trim() === '') {
          return <br key={index} />;
        }
        return <p key={index} className="text-gray-700 dark:text-gray-300 mt-3 text-lg leading-relaxed">{line}</p>;
      });
  };

  const renderYouTubeVideos = (resources) => {
    if (!resources) return null;
    
    const lines = resources.split('\n');
    const videos = [];
    
    lines.forEach((line, index) => {
      // Match YouTube links in the format: [title](https://www.youtube.com/watch?v=VIDEO_ID)
      const youtubeMatch = line.match(/\[([^\]]+)\]\((https?:\/\/(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+))\)/);
      
      // Match YouTube iframe embeds
      const iframeMatch = line.match(/src=(['"])https?:\/\/(www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)\1/);
      
      if (youtubeMatch) {
        const [, title, , , videoId] = youtubeMatch;
        const videoDetail = videoDetails[videoId] || {};
        
        videos.push(
          <div key={index} className="my-8 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <div className="aspect-w-16 aspect-h-9">
              <iframe 
                src={`https://www.youtube.com/embed/${videoId}?rel=0`}
                title={videoDetail.title || title}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-full"
              ></iframe>
            </div>
            <div className="p-4">
              <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
                {videoDetail.title || title}
              </h3>
              {videoDetail.description && (
                <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-3">
                  {videoDetail.description}
                </p>
              )}
              <a 
                href={`https://www.youtube.com/watch?v=${videoId}`} 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center mt-3 text-blue-600 dark:text-blue-400 hover:underline"
              >
                Ver en YouTube <FiExternalLink className="ml-1" />
              </a>
            </div>
          </div>
        );
      } else if (iframeMatch) {
        // Para iframes de YouTube
        const videoId = iframeMatch[3];
        const videoDetail = videoDetails[videoId] || {};
        
        videos.push(
          <div key={index} className="my-8 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <div className="aspect-w-16 aspect-h-9">
              <iframe 
                src={`https://www.youtube.com/embed/${videoId}?rel=0`}
                title={videoDetail.title || `Video ${index + 1}`}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-full"
              ></iframe>
            </div>
            <div className="p-4">
              <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
                {videoDetail.title || `Video ${index + 1}`}
              </h3>
              {videoDetail.description && (
                <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-3">
                  {videoDetail.description}
                </p>
              )}
              <a 
                href={`https://www.youtube.com/watch?v=${videoId}`} 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center mt-3 text-blue-600 dark:text-blue-400 hover:underline"
              >
                Ver en YouTube <FiExternalLink className="ml-1" />
              </a>
            </div>
          </div>
        );
      } else if (line.includes('<iframe') && line.includes('youtube.com/embed')) {
        // Para líneas que contienen iframe pero no se pudieron parsear correctamente
        videos.push(
          <div key={index} className="my-8 bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
            <div className="aspect-w-16 aspect-h-9" dangerouslySetInnerHTML={createMarkup(line)} />
          </div>
        );
      } else if (line.trim() !== '') {
        // Render non-YouTube content as regular markdown
        videos.push(
          <div key={index} className="my-2">
            {renderMarkdown(line)}
          </div>
        );
      }
    });
    
    if (videos.length === 0 && !loading) {
      return (
        <div className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">No hay recursos disponibles para este módulo</p>
        </div>
      );
    }
    
    return (
      <div className="space-y-6">
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        ) : (
          videos
        )}
      </div>
    );
  };
  
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-white dark:bg-gray-900 overflow-y-auto"
    >
      {/* Header */}
      <div className="sticky top-0 z-10 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              {course?.content?.titulo || course?.title}
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Módulo {currentModuleIndex + 1} de {modules.length}: {currentModule.titulo}
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <button
              onClick={onClose}
              className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              aria-label="Cerrar vista inmersiva"
            >
              <FiX size={20} />
            </button>
          </div>
        </div>
        
        {/* Module navigation tabs */}
        <div className="container mx-auto px-4 flex border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={() => setCurrentView('content')}
            className={`py-3 px-5 font-medium text-sm transition-colors ${
              currentView === 'content'
                ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            }`}
          >
            Contenido
          </button>
          <button
            onClick={() => setCurrentView('resources')}
            className={`py-3 px-5 font-medium text-sm transition-colors ${
              currentView === 'resources'
                ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400'
                : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            }`}
          >
            Recursos
          </button>
        </div>
      </div>
      
      {/* Content */}
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <AnimatePresence mode="wait">
          {currentView === 'content' ? (
            <motion.div
              key="content"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="prose dark:prose-invert max-w-none"
            >
              <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
                {currentModule.titulo}
              </h2>
              
              {renderMarkdown(currentModule.contenido)}
            </motion.div>
          ) : (
            <motion.div
              key="resources"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="prose dark:prose-invert max-w-none"
            >
              <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">
                Recursos del Módulo
              </h2>
              
              {renderYouTubeVideos(currentModule.recursos)}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {/* Navigation controls */}
      <div className="sticky bottom-0 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 py-4 px-4">
        <div className="container mx-auto flex justify-between items-center max-w-3xl">
          <button
            onClick={goToPreviousModule}
            disabled={currentModuleIndex === 0}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              currentModuleIndex === 0
                ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
                : 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/50'
            }`}
          >
            <FiArrowLeft size={16} />
            Módulo Anterior
          </button>
          
          <div className="text-center text-sm font-medium text-gray-500 dark:text-gray-400">
            {currentModuleIndex + 1} / {modules.length}
          </div>
          
          <button
            onClick={goToNextModule}
            disabled={currentModuleIndex === modules.length - 1}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              currentModuleIndex === modules.length - 1
                ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
                : 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-200 dark:hover:bg-blue-900/50'
            }`}
          >
            Siguiente Módulo
            <FiArrowRight size={16} />
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ImmersiveCourseView; 