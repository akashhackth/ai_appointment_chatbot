import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import Layout from '@/components/Layout';
import ChatWindow from '@/components/ChatWindow';

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <Layout>
      <div className="px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome, {user.fullName}!
            </h1>
            <p className="mt-2 text-gray-600">
              Chat with our AI assistant to book your appointment
            </p>
          </div>

          <div className="h-[600px]">
            <ChatWindow />
          </div>

          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">Quick Tips:</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Ask about available time slots</li>
              <li>• Book appointments by saying when you'd like to come</li>
              <li>• View your upcoming appointments</li>
              <li>• Cancel or reschedule existing appointments</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
}
