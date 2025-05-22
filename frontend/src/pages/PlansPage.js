import React, { useState, useEffect } from 'react';
import { FiCheck, FiStar } from 'react-icons/fi';
import Layout from '../components/Layout';
import { useAuth } from '../hooks/useAuth';
import { subscriptionService } from '../services/subscription';
import { useNavigate } from 'react-router-dom';

const PlansPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);

  useEffect(() => {
    const fetchPlans = async () => {
      try {
        setLoading(true);

        // Obtener los planes disponibles
        const plansData = await subscriptionService.getPlans();
        
        // Obtener el estado de suscripción actual
        const subscriptionData = await subscriptionService.getSubscription();

        setPlans(plansData);
        setSubscriptionStatus(subscriptionData);
        setCurrentPlan(user.plan);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching plan data:', err);
        setError('No se pudieron cargar los planes. Por favor, intenta de nuevo más tarde.');
        setLoading(false);
      }
    };

    fetchPlans();
  }, [user]);

  const handleSelectPlan = async (plan) => {
    try {
      if (plan.id === currentPlan) {
        return; // Ya tiene este plan
      }
      
      // Si es el plan gratuito, actualizamos directamente
      if (plan.id === 'free') {
        await subscriptionService.updatePlan(plan.id);
        
        // Actualizar el estado
        setCurrentPlan(plan.id);
        alert(`¡Te has suscrito al plan ${plan.name}!`);
        
        // Recargar la página para actualizar los datos del usuario
        window.location.reload();
      } else {
        // Para planes pagos, vamos a la página de simulación
        navigate('/simulated-payment', { 
          state: { 
            plan: plan.id,
            amount: plan.price,
            name: plan.name
          } 
        });
      }
    } catch (err) {
      console.error('Error al procesar el plan:', err);
      setError('Error al procesar la solicitud. Por favor, intenta de nuevo.');
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-neutral-900 mb-8">Planes de suscripción</h1>
          <div className="text-center py-12">Cargando planes...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-bold text-neutral-900 mb-4">Planes de suscripción</h1>
        
        {user && (
          <div className="mb-8 bg-white p-4 rounded-lg shadow-sm border border-neutral-200">
            <h2 className="text-lg font-medium text-neutral-700 mb-2">Tu suscripción actual</h2>
            <div className="flex flex-wrap gap-4">
              <div>
                <span className="text-sm font-medium text-neutral-500">Plan:</span>
                <span className="ml-2 text-neutral-900 font-medium">
                  {user.plan === 'pro' ? 'Pro' : 'Free'}
                </span>
              </div>
              {subscriptionStatus && (
                <>
                  <div>
                    <span className="text-sm font-medium text-neutral-500">Cursos usados:</span>
                    <span className="ml-2 text-neutral-900 font-medium">
                      {subscriptionStatus.course_limit === -1 
                        ? 'Ilimitados' 
                        : `${subscriptionStatus.course_limit} cursos`}
                    </span>
                  </div>
                  {subscriptionStatus.expiration && (
                    <div>
                      <span className="text-sm font-medium text-neutral-500">Vence:</span>
                      <span className="ml-2 text-neutral-900 font-medium">
                        {new Date(subscriptionStatus.expiration).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        )}
        
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
            <span>{error}</span>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-6 my-8">
          {plans.map((plan) => (
            <div 
              key={plan.id} 
              className={`border rounded-xl p-6 bg-white shadow-sm
                ${plan.id === 'pro' ? 'ring-2 ring-primary-500' : ''} 
                ${currentPlan === plan.id ? 'border-primary-500 bg-primary-50' : 'border-neutral-200'}`}
            >
              {plan.id === 'pro' && (
                <div className="flex items-center text-primary-700 mb-2">
                  <FiStar className="mr-1" />
                  <span className="text-sm font-medium">Más popular</span>
                </div>
              )}
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold text-neutral-900">{plan.name}</h3>
                {currentPlan === plan.id && (
                  <span className="px-2 py-1 bg-primary-100 text-primary-800 text-xs font-medium rounded-full">
                    Plan actual
                  </span>
                )}
              </div>
              <p className="text-3xl font-bold mb-4">
                ${plan.price.toFixed(2)}
                <span className="text-sm text-neutral-500 font-normal">/mes</span>
              </p>
              <ul className="space-y-4 mb-8">
                <li className="flex items-start">
                  <FiCheck className="text-green-500 mt-1 mr-2 flex-shrink-0" />
                  <span>{plan.course_limit === -1 ? 'Cursos ilimitados' : `${plan.course_limit} cursos`}</span>
                </li>
                <li className="flex items-start">
                  <FiCheck className="text-green-500 mt-1 mr-2 flex-shrink-0" />
                  <span>{plan.description}</span>
                </li>
                {plan.id === 'pro' && (
                  <li className="flex items-start">
                    <FiCheck className="text-green-500 mt-1 mr-2 flex-shrink-0" />
                    <span>Soporte prioritario</span>
                  </li>
                )}
              </ul>
              <button 
                onClick={() => handleSelectPlan(plan)}
                className={`w-full py-3 px-4 rounded-lg transition-colors 
                  ${currentPlan === plan.id
                    ? 'border border-primary-500 text-primary-700 bg-primary-50 hover:bg-primary-100'
                    : plan.id === 'pro'
                      ? 'bg-primary-600 text-white hover:bg-primary-700' 
                      : 'border border-neutral-300 text-neutral-700 bg-white hover:bg-neutral-50'
                  }
                  disabled:opacity-50 disabled:cursor-not-allowed
                `}
                disabled={currentPlan === plan.id}
              >
                {currentPlan === plan.id 
                  ? 'Plan actual' 
                  : 'Seleccionar plan'}
              </button>
            </div>
          ))}
        </div>

        <div className="bg-white p-6 rounded-lg border border-neutral-200 mb-8">
          <h2 className="text-xl font-semibold text-neutral-900 mb-4">Preguntas frecuentes</h2>
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-neutral-900 mb-2">¿Cómo funciona la facturación?</h3>
              <p className="text-neutral-700">
                Los planes se facturan mensualmente. Puedes cancelar tu suscripción en cualquier momento.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-medium text-neutral-900 mb-2">¿Puedo cambiar de plan?</h3>
              <p className="text-neutral-700">
                Sí, puedes actualizar o degradar tu plan en cualquier momento. Los cambios se aplicarán inmediatamente.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-medium text-neutral-900 mb-2">¿Qué pasa con mis cursos si cancelo?</h3>
              <p className="text-neutral-700">
                Tus cursos existentes permanecerán en tu cuenta, pero no podrás crear nuevos cursos si excedes el límite de tu plan.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default PlansPage; 