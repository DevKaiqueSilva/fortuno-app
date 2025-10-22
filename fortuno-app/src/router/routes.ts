import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      { path: '', component: () => import('pages/AuthPage.vue') },
      { path: '/login', component: () => import('pages/LoginPage.vue') },
      { path: '/register', component: () => import('pages/UserRegisterPage.vue') },
    ],
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'dashboard', component: () => import('pages/DashboardPage.vue') },
      { 
        path: '/wallet',
        name: 'wallet',
        component: () => import('pages/WalletPage.vue'),
      },
      {
        path: '/wallet/:code',
        name: 'wallet-detail',
        component: () => import('pages/WalletDetailPage.vue'),
      },
      {
        path: '/transactions',
        name: 'transactions',
        component: () => import('pages/TransactionsPage.vue'),
      },
      {
        path: '/categories',
        name: 'categories',
        component: () => import('pages/CategoryPage.vue'),
      },
      { path: '/profile', name: 'profile', component: () => import('pages/ProfilePage.vue') },
      { path: '/profile-info', name: 'profile-info', component: () => import('pages/ProfileInfoPage.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
