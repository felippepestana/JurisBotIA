import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  eslint: {
    // Linting is handled via separate CI step
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Type checking is handled via separate CI step
    ignoreBuildErrors: false,
  },
}

export default nextConfig
