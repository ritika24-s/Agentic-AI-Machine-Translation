/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/translate/:path*',
        destination: 'http://localhost:8000/:path*', // FastAPI backend
      },
    ]
  },
  experimental: {
    appDir: true,
  },
}

module.exports = nextConfig