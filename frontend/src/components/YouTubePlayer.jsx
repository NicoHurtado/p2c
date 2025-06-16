import React, { useState } from 'react';
import { Play, ExternalLink, Clock, User } from 'lucide-react';

const YouTubePlayer = ({ video, autoplay = false }) => {
  const [isExpanded, setIsExpanded] = useState(autoplay);

  if (!video) return null;

  const embedUrl = `https://www.youtube.com/embed/${video.video_id}?rel=0&modestbranding=1${autoplay ? '&autoplay=1' : ''}`;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden mb-4">
      {/* Video header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-start gap-3">
          <img 
            src={video.thumbnail_url} 
            alt={video.title}
            className="w-24 h-16 object-cover rounded cursor-pointer"
            onClick={() => setIsExpanded(!isExpanded)}
          />
          <div className="flex-1">
            <h3 className="font-semibold text-gray-800 mb-1 line-clamp-2">
              {video.title}
            </h3>
            <div className="flex items-center gap-4 text-sm text-gray-600 mb-2">
              <div className="flex items-center gap-1">
                <User size={14} />
                <span>{video.channel_name}</span>
              </div>
              {video.duration && (
                <div className="flex items-center gap-1">
                  <Clock size={14} />
                  <span>{video.duration}</span>
                </div>
              )}
            </div>
            {video.description && (
              <p className="text-sm text-gray-600 line-clamp-2 mb-2">
                {video.description}
              </p>
            )}
          </div>
          <div className="flex flex-col gap-2">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex items-center gap-2 px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <Play size={16} />
              {isExpanded ? 'Ocultar' : 'Ver'}
            </button>
            <a
              href={video.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ExternalLink size={16} />
              YouTube
            </a>
          </div>
        </div>
      </div>

      {/* Video player */}
      {isExpanded && (
        <div className="aspect-video">
          <iframe
            src={embedUrl}
            title={video.title}
            className="w-full h-full"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      )}
    </div>
  );
};

export default YouTubePlayer; 