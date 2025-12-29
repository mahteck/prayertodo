'use client'

export default function Footer() {
  return (
    <footer className="bg-black border-t border-[#2A2A2A] mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About Section */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <span className="text-3xl">🕌</span>
              <span className="text-xl font-bold text-salaat-orange">SalaatFlow</span>
            </div>
            <p className="text-gray-400 text-sm">
              Your Islamic task management companion for organizing spiritual activities and prayers.
            </p>
          </div>

          {/* Contact Section */}
          <div>
            <h3 className="text-white font-semibold mb-4">Contact Us</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center text-gray-400">
                <svg className="w-4 h-4 mr-2 text-salaat-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <a href="mailto:mahteckteach@gmail.com" className="hover:text-salaat-orange transition-colors">
                  mahteckteach@gmail.com
                </a>
              </div>
              <div className="flex items-center text-gray-400">
                <svg className="w-4 h-4 mr-2 text-salaat-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <a href="tel:03010325593" className="hover:text-salaat-orange transition-colors">
                  03010325593
                </a>
              </div>
              <div className="flex items-center text-gray-400">
                <svg className="w-4 h-4 mr-2 text-salaat-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
                <a href="https://mahteck.com" target="_blank" rel="noopener noreferrer" className="hover:text-salaat-orange transition-colors">
                  mahteck.com
                </a>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <div className="space-y-2 text-sm">
              <a href="/" className="block text-gray-400 hover:text-salaat-orange transition-colors">
                Home
              </a>
              <a href="/tasks" className="block text-gray-400 hover:text-salaat-orange transition-colors">
                Tasks
              </a>
              <a href="/masjids" className="block text-gray-400 hover:text-salaat-orange transition-colors">
                Masjids
              </a>
              <a href="/hadith" className="block text-gray-400 hover:text-salaat-orange transition-colors">
                Daily Hadith
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-[#2A2A2A] mt-8 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-500 text-sm">
            © {new Date().getFullYear()} SalaatFlow. All rights reserved.
          </p>
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <p className="text-gray-500 text-sm">
              Developed by{' '}
              <a href="https://mahteck.com" target="_blank" rel="noopener noreferrer" className="text-salaat-orange hover:text-salaat-orange-light transition-colors">
                Mahteck
              </a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
