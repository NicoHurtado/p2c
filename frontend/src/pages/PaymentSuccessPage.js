import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FiCheck } from 'react-icons/fi';
import Layout from '../components/Layout';
import { useAuth } from '../hooks/useAuth';

const PaymentSuccessPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();

  // Obtener el plan del state si está disponible
  const { plan, name } = location.state || {};

  // Redirigir si no hay plan
  useEffect(() => {
    if (!plan) {
      navigate('/plans');
    }

    // Recargar la página después de 3 segundos para actualizar los datos del usuario
    const timer = setTimeout(() => {
      window.location.reload();
    }, 3000);

    return () => clearTimeout(timer);
  }, [plan, navigate]);

  if (!plan) {
    return null;
  }

  const planName = name || (plan === 'pro' ? 'Pro' : 'Free');

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white shadow-sm rounded-lg p-8 text-center">
          <div className="py-8">
            <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100">
              <FiCheck className="h-8 w-8 text-green-600" />
            </div>
            <h2 className="mt-4 text-xl font-semibold text-neutral-900">¡Pago exitoso!</h2>
            <p className="mt-2 text-neutral-600">Tu pago ha sido procesado correctamente.</p>
            <div className="mt-6 bg-primary-50 rounded-lg p-4 inline-block">
              <p className="text-primary-700 font-medium">
                Tu plan <span className="font-bold">{planName}</span> ya está activo
              </p>
            </div>
            <div className="mt-8">
              <button
                onClick={() => navigate('/dashboard')}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
              >
                Ir al dashboard
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default PaymentSuccessPage; 