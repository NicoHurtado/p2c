import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FiChevronDown, FiX, FiMenu, FiLogIn, FiUserPlus } from 'react-icons/fi';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Manejo del scroll para cambiar la apariencia de la navbar
  useEffect(() => {
    const handleScroll = () => {
      const offset = window.scrollY;
      setScrolled(offset > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Función para scroll suave a secciones
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
    setIsOpen(false);
  };

  const navbarClasses = `fixed w-full z-50 transition-all duration-300 ${
    scrolled ? 'bg-white/80 backdrop-blur-lg shadow-lg' : 'bg-transparent'
  }`;

  const dropdownVariants = {
    hidden: { opacity: 0, y: -5 },
    visible: { opacity: 1, y: 0 },
  };

  const mobileMenuVariants = {
    hidden: { opacity: 0, x: '100%' },
    visible: { opacity: 1, x: 0 },
  };

  return (
    <nav className={navbarClasses}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <Link to="/" className="flex-shrink-0">
            <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-primary-700">
              Prompt2Course
            </h1>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex md:items-center md:space-x-8">
            {/* Cursos Dropdown */}
            <div className="relative">
              <button
                onMouseEnter={() => setShowDropdown(true)}
                onMouseLeave={() => setShowDropdown(false)}
                className="flex items-center space-x-1 text-neutral-700 hover:text-primary-600 transition-colors"
              >
                <span>Cursos</span>
                <FiChevronDown className={`transform transition-transform ${showDropdown ? 'rotate-180' : ''}`} />
              </button>

              <AnimatePresence>
                {showDropdown && (
                  <motion.div
                    initial="hidden"
                    animate="visible"
                    exit="hidden"
                    variants={dropdownVariants}
                    className="absolute left-0 mt-2 w-56 rounded-xl bg-white shadow-lg ring-1 ring-black ring-opacity-5"
                    onMouseEnter={() => setShowDropdown(true)}
                    onMouseLeave={() => setShowDropdown(false)}
                  >
                    <div className="py-2 px-4 space-y-2">
                      <Link to="/cursos/populares" className="block text-sm text-neutral-700 hover:text-primary-600 hover:bg-neutral-50 rounded-lg px-3 py-2 transition-colors">
                        Categorías populares
                      </Link>
                      <Link to="/cursos/recientes" className="block text-sm text-neutral-700 hover:text-primary-600 hover:bg-neutral-50 rounded-lg px-3 py-2 transition-colors">
                        Cursos recientes
                      </Link>
                      <Link to="/cursos/recomendados" className="block text-sm text-neutral-700 hover:text-primary-600 hover:bg-neutral-50 rounded-lg px-3 py-2 transition-colors">
                        Cursos recomendados
                      </Link>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Smooth Scroll Links */}
            <button
              onClick={() => scrollToSection('como-funciona')}
              className="text-neutral-700 hover:text-primary-600 transition-colors"
            >
              Cómo funciona
            </button>
            <button
              onClick={() => scrollToSection('testimonios')}
              className="text-neutral-700 hover:text-primary-600 transition-colors"
            >
              Testimonios
            </button>

            {/* Regular Links */}
            <Link to="/planes" className="text-neutral-700 hover:text-primary-600 transition-colors">
              Planes
            </Link>
            <Link to="/contacto" className="text-neutral-700 hover:text-primary-600 transition-colors">
              Contacto
            </Link>

            {/* Auth Buttons */}
            <div className="flex items-center space-x-4 ml-4 border-l border-neutral-200 pl-4">
              <Link
                to="/login"
                className="flex items-center px-4 py-2 text-primary-600 hover:text-primary-700 transition-colors font-medium"
              >
                <FiLogIn className="mr-2" />
                Iniciar sesión
              </Link>
              <Link
                to="/register"
                className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-xl shadow-lg shadow-primary-600/20 hover:bg-primary-700 hover:shadow-primary-600/30 transition-all transform hover:scale-105 font-medium"
              >
                <FiUserPlus className="mr-2" />
                Registrarse
              </Link>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-neutral-700 hover:text-primary-600 hover:bg-neutral-100 transition-colors"
            >
              {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial="hidden"
            animate="visible"
            exit="hidden"
            variants={mobileMenuVariants}
            className="md:hidden fixed inset-0 z-50 bg-white"
          >
            <div className="pt-16 pb-6 px-4 space-y-6">
              <button
                onClick={() => setIsOpen(false)}
                className="absolute top-4 right-4 p-2 rounded-md text-neutral-700 hover:text-primary-600 hover:bg-neutral-100 transition-colors"
              >
                <FiX size={24} />
              </button>

              {/* Mobile Navigation Links */}
              <div className="space-y-6">
                <div className="space-y-2">
                  <h3 className="text-sm font-semibold text-neutral-900 uppercase tracking-wider">Cursos</h3>
                  <div className="space-y-2">
                    <Link
                      to="/cursos/populares"
                      className="block text-base text-neutral-700 hover:text-primary-600"
                      onClick={() => setIsOpen(false)}
                    >
                      Categorías populares
                    </Link>
                    <Link
                      to="/cursos/recientes"
                      className="block text-base text-neutral-700 hover:text-primary-600"
                      onClick={() => setIsOpen(false)}
                    >
                      Cursos recientes
                    </Link>
                    <Link
                      to="/cursos/recomendados"
                      className="block text-base text-neutral-700 hover:text-primary-600"
                      onClick={() => setIsOpen(false)}
                    >
                      Cursos recomendados
                    </Link>
                  </div>
                </div>

                <button
                  onClick={() => {
                    scrollToSection('como-funciona');
                    setIsOpen(false);
                  }}
                  className="block w-full text-left text-base text-neutral-700 hover:text-primary-600"
                >
                  Cómo funciona
                </button>
                <button
                  onClick={() => {
                    scrollToSection('testimonios');
                    setIsOpen(false);
                  }}
                  className="block w-full text-left text-base text-neutral-700 hover:text-primary-600"
                >
                  Testimonios
                </button>
                <Link
                  to="/planes"
                  className="block text-base text-neutral-700 hover:text-primary-600"
                  onClick={() => setIsOpen(false)}
                >
                  Planes
                </Link>
                <Link
                  to="/contacto"
                  className="block text-base text-neutral-700 hover:text-primary-600"
                  onClick={() => setIsOpen(false)}
                >
                  Contacto
                </Link>

                {/* Mobile Auth Buttons */}
                <div className="pt-6 space-y-4">
                  <Link
                    to="/login"
                    className="flex items-center justify-center w-full px-4 py-3 text-primary-600 hover:text-primary-700 border-2 border-primary-600 rounded-xl font-medium transition-colors"
                    onClick={() => setIsOpen(false)}
                  >
                    <FiLogIn className="mr-2" />
                    Iniciar sesión
                  </Link>
                  <Link
                    to="/register"
                    className="flex items-center justify-center w-full px-4 py-3 bg-primary-600 text-white rounded-xl shadow-lg shadow-primary-600/20 hover:bg-primary-700 hover:shadow-primary-600/30 transition-all transform hover:scale-105 font-medium"
                    onClick={() => setIsOpen(false)}
                  >
                    <FiUserPlus className="mr-2" />
                    Registrarse
                  </Link>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar; 