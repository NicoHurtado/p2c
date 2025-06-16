import React from 'react';
import { Code, ExternalLink, Lightbulb, AlertTriangle, CheckCircle } from 'lucide-react';

const MarkdownRenderer = ({ content }) => {
  if (!content) return null;

  // 🎨 STYLES - Pure CSS objects to replace Tailwind
  const styles = {
    container: {
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      lineHeight: 1.7,
      color: '#1f2937',
      fontSize: '16px'
    },
    h1: {
      fontSize: '2rem',
      fontWeight: '700',
      color: '#111827',
      marginBottom: '1.5rem',
      marginTop: '2rem',
      paddingBottom: '0.75rem',
      borderBottom: '2px solid #e5e7eb'
    },
    h2: {
      fontSize: '1.5rem',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '1rem',
      marginTop: '1.5rem',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem'
    },
    h3: {
      fontSize: '1.25rem',
      fontWeight: '600',
      color: '#374151',
      marginBottom: '0.75rem',
      marginTop: '1.25rem'
    },
    h4: {
      fontSize: '1.125rem',
      fontWeight: '600',
      color: '#4b5563',
      marginBottom: '0.5rem',
      marginTop: '1rem'
    },
    p: {
      marginBottom: '1rem',
      color: '#374151'
    },
    strong: {
      fontWeight: '600',
      color: '#111827'
    },
    em: {
      fontStyle: 'italic',
      color: '#6b7280'
    },
    ul: {
      listStyle: 'none',
      marginBottom: '1rem',
      paddingLeft: '1.5rem',
      color: '#374151'
    },
    ol: {
      listStyle: 'decimal',
      marginBottom: '1rem',
      paddingLeft: '1.5rem',
      color: '#374151'
    },
    li: {
      marginBottom: '0.5rem',
      position: 'relative'
    },
    ulLi: {
      paddingLeft: '1rem'
    },
    ulLiBefore: {
      content: '""',
      position: 'absolute',
      left: '-1rem',
      top: '0.5rem',
      width: '6px',
      height: '6px',
      borderRadius: '50%',
      background: '#3b82f6'
    },
    code: {
      background: '#f1f5f9',
      color: '#dc2626',
      padding: '0.125rem 0.375rem',
      borderRadius: '0.25rem',
      fontSize: '0.875rem',
      fontFamily: "'Consolas', 'Monaco', 'Courier New', monospace",
      border: '1px solid #e2e8f0'
    },
    pre: {
      background: '#1f2937',
      color: '#f9fafb',
      padding: '1.5rem',
      borderRadius: '0.75rem',
      marginBottom: '1.5rem',
      overflow: 'auto',
      fontSize: '0.875rem',
      fontFamily: "'Consolas', 'Monaco', 'Courier New', monospace",
      border: '1px solid #374151',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    },
    preCode: {
      background: 'transparent',
      color: 'inherit',
      padding: 0,
      border: 'none',
      fontSize: 'inherit',
      fontFamily: 'inherit'
    },
    blockquote: {
      background: 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
      borderLeft: '4px solid #3b82f6',
      padding: '1rem 1.5rem',
      marginBottom: '1.5rem',
      borderRadius: '0 0.5rem 0.5rem 0',
      color: '#1e40af',
      fontSize: '0.875rem',
      fontStyle: 'italic'
    },
    noteBox: {
      background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
      border: '1px solid #f59e0b',
      borderRadius: '0.75rem',
      padding: '1rem 1.5rem',
      marginBottom: '1.5rem',
      position: 'relative'
    },
    noteTitle: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      fontWeight: '600',
      color: '#92400e',
      marginBottom: '0.5rem',
      fontSize: '0.875rem'
    },
    noteContent: {
      color: '#78350f',
      fontSize: '0.875rem',
      lineHeight: 1.6
    },
    warningBox: {
      background: 'linear-gradient(135deg, #fecaca 0%, #fca5a5 100%)',
      border: '1px solid #ef4444',
      borderRadius: '0.75rem',
      padding: '1rem 1.5rem',
      marginBottom: '1.5rem'
    },
    warningTitle: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      fontWeight: '600',
      color: '#991b1b',
      marginBottom: '0.5rem',
      fontSize: '0.875rem'
    },
    warningContent: {
      color: '#7f1d1d',
      fontSize: '0.875rem',
      lineHeight: 1.6
    },
    successBox: {
      background: 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)',
      border: '1px solid #10b981',
      borderRadius: '0.75rem',
      padding: '1rem 1.5rem',
      marginBottom: '1.5rem'
    },
    successTitle: {
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      fontWeight: '600',
      color: '#065f46',
      marginBottom: '0.5rem',
      fontSize: '0.875rem'
    },
    successContent: {
      color: '#064e3b',
      fontSize: '0.875rem',
      lineHeight: 1.6
    },
    codeBlock: {
      position: 'relative'
    },
    codeHeader: {
      background: '#374151',
      color: '#d1d5db',
      padding: '0.5rem 1rem',
      fontSize: '0.75rem',
      fontWeight: '500',
      borderTopLeftRadius: '0.75rem',
      borderTopRightRadius: '0.75rem',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      borderBottom: '1px solid #4b5563'
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse',
      marginBottom: '1.5rem',
      background: 'white',
      borderRadius: '0.5rem',
      overflow: 'hidden',
      boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
    },
    th: {
      background: '#f8fafc',
      padding: '0.75rem',
      textAlign: 'left',
      fontWeight: '600',
      color: '#374151',
      borderBottom: '2px solid #e5e7eb',
      fontSize: '0.875rem'
    },
    td: {
      padding: '0.75rem',
      borderBottom: '1px solid #f1f5f9',
      color: '#6b7280',
      fontSize: '0.875rem'
    },
    link: {
      color: '#2563eb',
      textDecoration: 'underline',
      fontWeight: '500',
      transition: 'color 0.2s ease'
    },
    linkHover: {
      color: '#1d4ed8'
    }
  };

  // Process content to handle special formatting
  const processContent = (htmlContent) => {
    if (!htmlContent) return '';

    let processed = htmlContent;

    // Handle code blocks with language
    processed = processed.replace(
      /<pre><code class="language-(\w+)">([\s\S]*?)<\/code><\/pre>/g,
      (match, lang, code) => {
        return `
          <div style="${Object.entries(styles.codeBlock).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
            <div style="${Object.entries(styles.codeHeader).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
              <span style="margin-right: 0.5rem;">💻</span> ${lang.toUpperCase()}
            </div>
            <pre style="${Object.entries(styles.pre).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}; border-top-left-radius: 0; border-top-right-radius: 0; margin-bottom: 0;">
              <code style="${Object.entries(styles.preCode).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">${code}</code>
            </pre>
          </div>
        `;
      }
    );

    // Handle special note boxes
    processed = processed.replace(
      /📝\s*<strong>Nota:<\/strong>\s*(.*?)(?=<p>|$)/gi,
      (match, content) => {
        return `
          <div style="${Object.entries(styles.noteBox).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
            <div style="${Object.entries(styles.noteTitle).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
              💡 Nota Importante
            </div>
            <div style="${Object.entries(styles.noteContent).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">${content}</div>
          </div>
        `;
      }
    );

    // Handle warnings
    processed = processed.replace(
      /⚠️\s*<strong>Advertencia:<\/strong>\s*(.*?)(?=<p>|$)/gi,
      (match, content) => {
        return `
          <div style="${Object.entries(styles.warningBox).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
            <div style="${Object.entries(styles.warningTitle).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
              ⚠️ Advertencia
            </div>
            <div style="${Object.entries(styles.warningContent).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">${content}</div>
          </div>
        `;
      }
    );

    // Handle success/tips
    processed = processed.replace(
      /✅\s*<strong>Tip:<\/strong>\s*(.*?)(?=<p>|$)/gi,
      (match, content) => {
        return `
          <div style="${Object.entries(styles.successBox).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
            <div style="${Object.entries(styles.successTitle).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">
              ✅ Consejo Útil
            </div>
            <div style="${Object.entries(styles.successContent).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">${content}</div>
          </div>
        `;
      }
    );

    return processed;
  };

  const processedContent = processContent(content);

  // Apply global styles to HTML elements
  const applyStyles = (html) => {
    let styledHtml = html;

    // Apply heading styles
    styledHtml = styledHtml.replace(
      /<h1>/g,
      `<h1 style="${Object.entries(styles.h1).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    styledHtml = styledHtml.replace(
      /<h2>/g,
      `<h2 style="${Object.entries(styles.h2).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    styledHtml = styledHtml.replace(
      /<h3>/g,
      `<h3 style="${Object.entries(styles.h3).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    styledHtml = styledHtml.replace(
      /<h4>/g,
      `<h4 style="${Object.entries(styles.h4).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply paragraph styles
    styledHtml = styledHtml.replace(
      /<p>/g,
      `<p style="${Object.entries(styles.p).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply strong styles
    styledHtml = styledHtml.replace(
      /<strong>/g,
      `<strong style="${Object.entries(styles.strong).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply em styles
    styledHtml = styledHtml.replace(
      /<em>/g,
      `<em style="${Object.entries(styles.em).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply list styles
    styledHtml = styledHtml.replace(
      /<ul>/g,
      `<ul style="${Object.entries(styles.ul).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    styledHtml = styledHtml.replace(
      /<ol>/g,
      `<ol style="${Object.entries(styles.ol).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    
    // Handle list items specially for bullet points
    styledHtml = styledHtml.replace(
      /<li>/g,
      `<li style="${Object.entries({...styles.li, ...styles.ulLi}).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply code styles
    styledHtml = styledHtml.replace(
      /<code(?![^>]*class="language-)/g,
      `<code style="${Object.entries(styles.code).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply pre styles (for code blocks without custom processing)
    styledHtml = styledHtml.replace(
      /<pre(?![^>]*style=)/g,
      `<pre style="${Object.entries(styles.pre).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply blockquote styles
    styledHtml = styledHtml.replace(
      /<blockquote>/g,
      `<blockquote style="${Object.entries(styles.blockquote).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply table styles
    styledHtml = styledHtml.replace(
      /<table>/g,
      `<table style="${Object.entries(styles.table).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    styledHtml = styledHtml.replace(
      /<th>/g,
      `<th style="${Object.entries(styles.th).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );
    styledHtml = styledHtml.replace(
      /<td>/g,
      `<td style="${Object.entries(styles.td).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}">`
    );

    // Apply link styles
    styledHtml = styledHtml.replace(
      /<a /g,
      `<a style="${Object.entries(styles.link).map(([k, v]) => `${k.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join('; ')}" `
    );

    return styledHtml;
  };

  const finalContent = applyStyles(processedContent);

  return (
    <div 
      style={styles.container}
      dangerouslySetInnerHTML={{ __html: finalContent }}
    />
  );
};

export default MarkdownRenderer; 