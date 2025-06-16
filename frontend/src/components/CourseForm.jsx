import React, { useState } from 'react';
import { Plus, X, Send, BookOpen, Target, Heart } from 'lucide-react';

const CourseForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    prompt: '',
    level: 'principiante',
    interests: []
  });
  const [currentInterest, setCurrentInterest] = useState('');

  const handlePromptChange = (e) => {
    setFormData(prev => ({ ...prev, prompt: e.target.value }));
  };

  const handleLevelChange = (e) => {
    setFormData(prev => ({ ...prev, level: e.target.value }));
  };

  const addInterest = () => {
    if (currentInterest.trim() && !formData.interests.includes(currentInterest.trim())) {
      setFormData(prev => ({
        ...prev,
        interests: [...prev.interests, currentInterest.trim()]
      }));
      setCurrentInterest('');
    }
  };

  const removeInterest = (interest) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.filter(i => i !== interest)
    }));
  };

  const handleInterestKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addInterest();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validación más estricta
    const trimmedPrompt = formData.prompt.trim();
    
    if (!trimmedPrompt) {
      alert('Por favor describe qué quieres aprender');
      return;
    }
    
    if (!formData.level || !['principiante', 'intermedio', 'avanzado'].includes(formData.level)) {
      alert('Por favor selecciona un nivel válido');
      return;
    }
    
    // Asegurar que hay al menos un interés
    const finalInterests = formData.interests.length > 0 ? formData.interests : ['aprendizaje'];
    
    const finalFormData = {
      prompt: trimmedPrompt,
      level: formData.level,
      interests: finalInterests
    };
    
    // Log para debugging
    console.log('📤 Enviando datos del formulario:', finalFormData);
    console.log('📤 Tamaño del JSON:', JSON.stringify(finalFormData).length, 'bytes');
    
    onSubmit(finalFormData);
  };

  return (
    <div className="container-sm" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
      <div className="card">
        <div className="card-header text-center">
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            gap: '0.5rem',
            marginBottom: '1rem'
          }}>
            <BookOpen size={28} style={{ color: '#4f46e5' }} />
            <h2 className="text-2xl font-bold" style={{ margin: 0 }}>
              Crear Tu Curso Personalizado
            </h2>
          </div>
          <p className="text-gray-600">
            Describe qué quieres aprender y te crearemos un curso completo adaptado a ti
          </p>
        </div>

        <form onSubmit={handleSubmit} className="card-body">
          {/* Prompt Field */}
          <div className="form-group">
            <label className="form-label" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5rem' 
            }}>
              <Target size={16} style={{ color: '#4f46e5' }} />
              ¿Qué quieres aprender?
            </label>
            <textarea
              className="form-input form-textarea"
              value={formData.prompt}
              onChange={handlePromptChange}
              placeholder="Ejemplo: Quiero aprender machine learning aplicado a deportes porque me gusta el tenis y los videojuegos..."
              style={{ minHeight: '120px' }}
              disabled={isLoading}
            />
            <div className="text-sm text-gray-500 mt-2">
              💡 Sé específico sobre tus intereses y objetivos para obtener un mejor curso
            </div>
          </div>

          {/* Level Field */}
          <div className="form-group">
            <label className="form-label" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5rem' 
            }}>
              <BookOpen size={16} style={{ color: '#4f46e5' }} />
              Nivel de experiencia
            </label>
            <select
              className="form-input form-select"
              value={formData.level}
              onChange={handleLevelChange}
              disabled={isLoading}
            >
              <option value="principiante">🌱 Principiante - Empezando desde cero</option>
              <option value="intermedio">🚀 Intermedio - Tengo algo de experiencia</option>
              <option value="avanzado">⭐ Avanzado - Busco profundizar conocimientos</option>
            </select>
          </div>

          {/* Interests Field */}
          <div className="form-group">
            <label className="form-label" style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.5rem' 
            }}>
              <Heart size={16} style={{ color: '#4f46e5' }} />
              Intereses y hobbies (opcional)
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                className="form-input"
                value={currentInterest}
                onChange={(e) => setCurrentInterest(e.target.value)}
                onKeyPress={handleInterestKeyPress}
                placeholder="deportes, música, programación..."
                disabled={isLoading}
                style={{ flex: 1 }}
              />
              <button
                type="button"
                onClick={addInterest}
                className="btn btn-secondary"
                disabled={!currentInterest.trim() || isLoading}
              >
                <Plus size={16} />
              </button>
            </div>
            
            {formData.interests.length > 0 && (
              <div className="interest-tags">
                {formData.interests.map((interest, index) => (
                  <span key={index} className="interest-tag">
                    {interest}
                    <button
                      type="button"
                      onClick={() => removeInterest(interest)}
                      className="interest-tag-remove"
                      disabled={isLoading}
                    >
                      <X size={12} />
                    </button>
                  </span>
                ))}
              </div>
            )}
            
            <div className="text-sm text-gray-500 mt-2">
              ✨ Agregamos tus intereses para personalizar mejor el contenido
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-lg"
            disabled={isLoading || !formData.prompt.trim()}
            style={{ width: '100%', marginTop: '1rem' }}
          >
            {isLoading ? (
              <>
                <div className="loading-spinner" />
                Generando tu curso...
              </>
            ) : (
              <>
                <Send size={20} />
                Generar Mi Curso Personalizado
              </>
            )}
          </button>
        </form>

        <div className="card-footer text-center">
          <div className="text-sm text-gray-500">
            🤖 Powered by Claude AI • ⚡ Resultados en segundos
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseForm; 