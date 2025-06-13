# 🎨 **PROMPT2COURSE FRONTEND**

Frontend moderno y minimalista para el sistema Prompt2Course, construido con React y diseñado con un enfoque educativo.

## ✨ **CARACTERÍSTICAS**

### 🎯 **Funcionalidades Principales**
- **Formulario Interactivo**: Captura prompt, nivel y intereses del usuario
- **Pantallas de Carga Animadas**: Experiencia visual atractiva durante la generación
- **Visualización de Cursos**: Muestra el curso generado con diseño profesional
- **Responsive Design**: Funciona perfectamente en móviles y escritorio

### 🎨 **Diseño**
- **Minimalista y Moderno**: Paleta de colores educativa (azules, verdes, acentos dorados)
- **Animaciones Fluidas**: Usando Framer Motion para transiciones suaves
- **Tipografía Inter**: Fuente moderna y legible
- **Glassmorphism**: Efectos de transparencia y blur modernos

### 🔧 **Tecnologías**
- **React 18**: Framework principal
- **Framer Motion**: Animaciones y transiciones
- **Lucide React**: Iconos modernos
- **Axios**: Cliente HTTP
- **CSS Variables**: Sistema de diseño consistente

## 🚀 **INSTALACIÓN Y USO**

### Prerrequisitos
- Node.js 16+ 
- npm o yarn
- Backend Prompt2Course ejecutándose en puerto 8000

### Instalación
```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

La aplicación se abrirá en `http://localhost:3000`

## 📱 **FLUJO DE USUARIO**

### 1. **Formulario de Entrada**
- Descripción del curso deseado (textarea amplio)
- Selector de nivel (Principiante, Intermedio, Avanzado)
- Tags de intereses (dinámicos, agregables)
- Validación en tiempo real

### 2. **Pantalla de Carga**
- Barra de progreso animada
- Íconos rotatorios por fases
- Mensajes descriptivos del proceso
- Datos curiosos sobre educación

### 3. **Visualización del Curso**
- Hero section con gradiente
- Información del curso (título, descripción, stats)
- Sección de temas principales
- Lista de módulos con cards interactivas
- Botones de acción (Comenzar, Descargar, Crear Otro)

## 🎨 **SISTEMA DE DISEÑO**

### Colores Principales
```css
--primary: #4f46e5      /* Azul educativo */
--secondary: #06b6d4    /* Cyan */
--accent: #10b981       /* Verde éxito */
--warning: #f59e0b      /* Amarillo */
--error: #ef4444        /* Rojo */
```

### Componentes
- `Header`: Navegación sticky con glassmorphism
- `CourseForm`: Formulario completo con validación
- `LoadingScreen`: Animaciones de carga interactivas
- `CourseDisplay`: Visualización elegante del curso generado

## 🔄 **INTEGRACIÓN CON BACKEND**

### Endpoint Principal
```javascript
POST /api/courses/generate
{
  "prompt": "string",
  "level": "beginner|intermediate|advanced", 
  "interests": ["array", "of", "strings"]
}
```

### Proxy Configuration
El frontend incluye un proxy a `http://localhost:8000` para desarrollo.

## 📦 **ESTRUCTURA DEL PROYECTO**

```
frontend/
├── public/
│   └── index.html              # HTML base con fonts
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Cabecera con branding
│   │   ├── CourseForm.jsx      # Formulario principal
│   │   ├── LoadingScreen.jsx   # Pantalla de carga
│   │   └── CourseDisplay.jsx   # Visualización de curso
│   ├── styles/
│   │   └── global.css          # Estilos globales
│   ├── App.jsx                 # Componente principal
│   └── index.js                # Punto de entrada
├── package.json                # Dependencias
└── README.md                   # Documentación
```

## 🎯 **PRÓXIMAS MEJORAS**

### Funcionalidades Planificadas
- [ ] Autenticación de usuarios
- [ ] Guardado de cursos favoritos
- [ ] Sistema de comentarios y ratings
- [ ] Compartir cursos en redes sociales
- [ ] Modo oscuro/claro
- [ ] Búsqueda de cursos existentes
- [ ] Player de video integrado
- [ ] Certificados de completación

### Mejoras Técnicas
- [ ] Testing con Jest y React Testing Library
- [ ] Storybook para componentes
- [ ] PWA capabilities
- [ ] Optimización de bundle
- [ ] Internacionalización (i18n)

## 🤝 **DESARROLLO**

### Scripts Disponibles
```bash
npm start      # Servidor de desarrollo
npm build      # Build de producción
npm test       # Ejecutar tests
npm eject      # Eyectar configuración (irreversible)
```

### Convenciones
- Componentes en PascalCase
- Archivos JSX con extensión `.jsx`
- Estilos inline para componentes específicos
- CSS global para utilidades y sistema de diseño

---

**🚀 Creado para hacer el aprendizaje más accesible y personalizado** 