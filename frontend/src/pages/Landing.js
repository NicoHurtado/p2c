import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, useAnimation } from 'framer-motion';
import { FiArrowRight, FiClock, FiBookOpen, FiSave, FiSearch, FiStar, FiUser, FiMessageCircle } from 'react-icons/fi';

// Import components
import TextScramble from '../components/TextScramble';
import GlowingOrb from '../components/GlowingOrb';
import TextCycler from '../components/TextCycler';
import ShinyButton from '../components/ShinyButton';
import BackgroundGrid from '../components/BackgroundGrid';
import AnimatedSearch from '../components/AnimatedSearch';
import Navbar from '../components/Navbar';

// Animation variants
const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
};

const slideInFromLeft = {
  hidden: { x: -60, opacity: 0 },
  visible: { x: 0, opacity: 1 }
};

const slideInFromRight = {
  hidden: { x: 60, opacity: 0 },
  visible: { x: 0, opacity: 1 }
};

const fadeInUp = {
  hidden: { y: 40, opacity: 0 },
  visible: { y: 0, opacity: 1 }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2
    }
  }
};

const Landing = () => {
  const controls = useAnimation();
  
  useEffect(() => {
    controls.start("visible");
  }, [controls]);
  
  const learningTopics = [
    "Inteligencia Artificial",
    "Programación",
    "Marketing Digital",
    "Diseño UX/UI",
    "Machine Learning",
    "Desarrollo Web"
  ];
  
  const rhythmPhrases = [
    "a tu propio ritmo",
    "cuando tú quieras",
    "donde tú decidas",
    "como más te guste",
    "sin presiones",
    "a tu manera"
  ];

  return (
    <motion.div 
      initial="hidden" 
      animate="visible" 
      className="min-h-screen bg-white text-neutral-800 overflow-hidden relative"
    >
      {/* Background Grid */}
      <BackgroundGrid dotColor="rgba(0, 0, 0, 0.1)" dotSpacing={30} />
      
      {/* Navbar */}
      <Navbar />

      {/* Hero Section */}
      <section className="relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-24 md:pt-24 md:pb-32">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8">
            <div className="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left">
              <motion.h1 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7 }}
                className="text-4xl tracking-tight font-bold text-neutral-900 sm:text-5xl md:text-6xl"
              >
                <motion.span 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="block"
                >
                  Aprende cualquier tema
                </motion.span>
                
                {/* Texto animado que cambia verticalmente */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5, delay: 0.7 }}
                  className="block mt-2 h-16 overflow-hidden"
                >
                  <TextCycler 
                    texts={rhythmPhrases}
                    interval={3000}
                    textClassName="text-5xl md:text-6xl font-bold text-primary-500 animated-glow"
                  />
                </motion.div>
              </motion.h1>
              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.7 }}
                className="mt-6 text-lg text-neutral-600"
              >
                <TextScramble 
                  text="Prompt2Course te permite generar cursos personalizados para aprender cualquier tema, adaptados a tu nivel de experiencia, gustos, personalidad y tiempo disponible."
                  delay={1000}
                  duration={1500}
                />
              </motion.p>
              
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 1.5 }}
                className="mt-8 sm:flex sm:justify-center lg:justify-start"
              >
                <Link to="/register">
                  <ShinyButton className="py-3 px-6 text-base flex items-center space-x-2">
                    <span>Comenzar gratis</span>
                    <FiArrowRight className="ml-2" />
                  </ShinyButton>
                </Link>
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="mt-3 sm:mt-0 sm:ml-3"
                >
                  <Link
                    to="/login"
                    className="inline-flex items-center px-6 py-3 border border-neutral-300 rounded-xl text-base font-medium text-neutral-700 bg-white hover:bg-neutral-100 transition-all"
                  >
                    Iniciar sesión
                  </Link>
                </motion.div>
              </motion.div>
            </div>
            
            {/* Lado derecho - Animación de búsqueda */}
            <div className="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center justify-center">
              {/* Componente de búsqueda animada */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                className="relative z-10 w-full max-w-lg"
              >
                <AnimatedSearch />
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* Cómo funciona Section */}
      <section id="como-funciona" className="py-20 bg-neutral-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="text-center mb-16"
          >
            <motion.h2 
              variants={fadeInUp}
              className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-4"
            >
              Cómo funciona la IA en tu aprendizaje
            </motion.h2>
            <motion.p 
              variants={fadeInUp}
              className="text-lg text-neutral-600 max-w-2xl mx-auto"
            >
              Nuestra plataforma utiliza inteligencia artificial avanzada para crear
              una experiencia de aprendizaje única y personalizada.
            </motion.p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: FiUser,
                title: "Perfil personalizado",
                description: "La IA analiza tus objetivos, nivel y estilo de aprendizaje"
              },
              {
                icon: FiBookOpen,
                title: "Contenido adaptativo",
                description: "Cursos que se ajustan a tu ritmo y necesidades específicas"
              },
              {
                icon: FiClock,
                title: "Aprendizaje eficiente",
                description: "Optimiza tu tiempo con lecciones enfocadas en tus metas"
              }
            ].map((item, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="bg-white p-6 rounded-2xl shadow-lg"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4 mx-auto">
                  <item.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-neutral-900 mb-2">
                  {item.title}
                </h3>
                <p className="text-neutral-600">
                  {item.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <motion.section 
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.2 }}
        variants={fadeIn}
        transition={{ duration: 0.5 }}
        className="bg-neutral-50 relative py-16 sm:py-24 overflow-hidden"
      >
        {/* Subtle background effect */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-600/10 rounded-full blur-3xl" />
        </div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <motion.div 
            variants={fadeInUp}
            transition={{ duration: 0.6 }}
            className="lg:text-center"
          >
            <motion.h2 
              variants={fadeInUp}
              className="text-base text-primary-600 font-semibold tracking-wide uppercase"
            >
              <TextScramble text="Características" delay={200} duration={1000} />
            </motion.h2>
            <motion.p 
              variants={fadeInUp}
              className="mt-2 text-3xl leading-8 font-bold tracking-tight text-neutral-900 sm:text-4xl"
            >
              Todo lo que necesitas para aprender eficientemente
            </motion.p>
            <motion.p 
              variants={fadeInUp}
              className="mt-4 max-w-2xl text-xl text-neutral-600 lg:mx-auto"
            >
              Prompt2Course simplifica el proceso de aprendizaje con herramientas intuitivas y recursos personalizados.
            </motion.p>
          </motion.div>

          <motion.div 
            variants={staggerContainer}
            transition={{ duration: 0.3, delayChildren: 0.3, staggerChildren: 0.2 }}
            className="mt-16"
          >
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              {/* Feature 1 */}
              <motion.div 
                variants={fadeInUp}
                whileHover={{ y: -10, transition: { duration: 0.2 } }}
                className="bg-white backdrop-blur-sm rounded-2xl p-8 border border-neutral-200 shadow-xl"
              >
                <div>
                  <motion.div 
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: "spring", stiffness: 300 }}
                    className="flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white"
                  >
                    <FiBookOpen className="h-6 w-6" />
                  </motion.div>
                  <div className="mt-5">
                    <h3 className="text-xl font-medium text-neutral-900">Cursos personalizados</h3>
                    <p className="mt-2 text-base text-neutral-600">
                      Genera cursos completos y personalizados adaptados a tus necesidades específicas, nivel de experiencia y objetivo de aprendizaje.
                    </p>
                  </div>
                </div>
              </motion.div>

              {/* Feature 2 */}
              <motion.div 
                variants={fadeInUp}
                whileHover={{ y: -10, transition: { duration: 0.2 } }}
                className="bg-white backdrop-blur-sm rounded-2xl p-8 border border-neutral-200 shadow-xl"
              >
                <div>
                  <motion.div 
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: "spring", stiffness: 300 }}
                    className="flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white"
                  >
                    <FiClock className="h-6 w-6" />
                  </motion.div>
                  <div className="mt-5">
                    <h3 className="text-xl font-medium text-neutral-900">Eficiente</h3>
                    <p className="mt-2 text-base text-neutral-600">
                      Obtén rápidamente contenido estructurado sin tener que buscar en múltiples fuentes o diseñar tu propio plan de estudio.
                    </p>
                  </div>
                </div>
              </motion.div>

              {/* Feature 3 */}
              <motion.div 
                variants={fadeInUp}
                whileHover={{ y: -10, transition: { duration: 0.2 } }}
                className="bg-white backdrop-blur-sm rounded-2xl p-8 border border-neutral-200 shadow-xl"
              >
                <div>
                  <motion.div 
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: "spring", stiffness: 300 }}
                    className="flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white"
                  >
                    <FiSave className="h-6 w-6" />
                  </motion.div>
                  <div className="mt-5">
                    <h3 className="text-xl font-medium text-neutral-900">Biblioteca personal</h3>
                    <p className="mt-2 text-base text-neutral-600">
                      Guarda tus cursos generados en tu biblioteca personal y accede a ellos cuando quieras, desde cualquier dispositivo.
                    </p>
                  </div>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* Testimonios Section */}
      <section id="testimonios" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={staggerContainer}
            className="text-center mb-16"
          >
            <motion.h2 
              variants={fadeInUp}
              className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-4"
            >
              Lo que dicen nuestros estudiantes
            </motion.h2>
            <motion.p 
              variants={fadeInUp}
              className="text-lg text-neutral-600 max-w-2xl mx-auto"
            >
              Descubre cómo Prompt2Course está transformando la educación online
            </motion.p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                name: "Ana García",
                role: "Estudiante de Marketing Digital",
                content: "La personalización del contenido es increíble. Cada lección se adapta perfectamente a mi nivel y objetivos.",
                avatar: "AG"
              },
              {
                name: "Carlos Rodríguez",
                role: "Desarrollador Frontend",
                content: "La IA realmente entiende cómo aprendo mejor. Los cursos son eficientes y muy prácticos.",
                avatar: "CR"
              },
              {
                name: "María López",
                role: "Diseñadora UX/UI",
                content: "Prompt2Course me ayudó a mejorar mis habilidades de diseño de manera estructurada y efectiva.",
                avatar: "ML"
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="bg-white p-6 rounded-2xl shadow-lg"
              >
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary-700 font-semibold">
                    {testimonial.avatar}
                  </div>
                  <div className="ml-4">
                    <h4 className="text-lg font-semibold text-neutral-900">
                      {testimonial.name}
                    </h4>
                    <p className="text-sm text-neutral-600">
                      {testimonial.role}
                    </p>
                  </div>
                </div>
                <p className="text-neutral-700">
                  {testimonial.content}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <motion.section 
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeIn}
        className="bg-gradient-to-r from-primary-500 to-primary-600 relative overflow-hidden"
      >
        <div className="absolute inset-0 overflow-hidden">
          <motion.div 
            className="absolute top-1/4 -right-20 w-80 h-80 bg-white/30 rounded-full blur-3xl"
            initial={{ opacity: 0.2 }}
            animate={{ opacity: 0.5 }}
            transition={{ duration: 8, repeat: Infinity, repeatType: 'reverse' }}
          />
          <div className="absolute bottom-1/4 -left-20 w-60 h-60 bg-white/20 rounded-full blur-3xl" />
        </div>
        
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between relative z-10">
          <motion.h2 
            variants={slideInFromLeft}
            className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl"
          >
            <span className="block">¿Listo para comenzar?</span>
            <span className="block text-primary-100">
              Únete a nuestra comunidad de aprendizaje
            </span>
          </motion.h2>
          <motion.div 
            variants={slideInFromRight}
            className="mt-8 flex lg:mt-0 lg:flex-shrink-0"
          >
            <Link to="/register">
              <ShinyButton primary={false} className="px-8 py-3 bg-white text-primary-600 hover:bg-primary-50">
                Comenzar ahora
              </ShinyButton>
            </Link>
          </motion.div>
        </div>
      </motion.section>

      {/* Footer */}
      <motion.footer 
        variants={fadeIn}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        className="bg-neutral-100 border-t border-neutral-200"
      >
        <div className="max-w-7xl mx-auto py-12 px-4 overflow-hidden sm:px-6 lg:px-8">
          <motion.p 
            variants={fadeInUp}
            className="mt-8 text-center text-base text-neutral-500"
          >
            &copy; {new Date().getFullYear()} Prompt2Course. Todos los derechos reservados.
          </motion.p>
        </div>
      </motion.footer>
    </motion.div>
  );
};

export default Landing; 