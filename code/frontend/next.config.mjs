/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  rewrites: async () => [
    {
      // Match everything in `/api` except `/api/auth` (handled by NextAuth.js)
      source: '/api/:path((?!auth).*)',
      destination: `${process.env.API_BASE}/:path*`,
    },
  ],
}

export default nextConfig
