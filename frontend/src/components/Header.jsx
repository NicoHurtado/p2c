import React from 'react';
import { GraduationCap, Sparkles } from 'lucide-react';

const Header = () => {
  return (
    <header style={{ 
      background: 'rgba(255, 255, 255, 0.95)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div className="container">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1rem 0',
          gap: '0.75rem'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
            borderRadius: '12px',
            padding: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <GraduationCap size={24} color="white" />
          </div>
          
          <h1 style={{
            fontSize: '1.5rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            margin: 0,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            Prompt2Course
            <Sparkles size={20} style={{ color: '#f59e0b' }} />
          </h1>
        </div>
        
        <div className="text-center" style={{ paddingBottom: '1rem' }}>
          <p className="text-gray-600" style={{ 
            fontSize: '0.875rem',
            margin: 0
          }}>
            🚀 Genera cursos personalizados con Inteligencia Artificial
          </p>
        </div>
      </div>
    </header>
  );
};

export default Header; 