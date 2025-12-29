# SalaatFlow Frontend

Next.js frontend application for Islamic task management system with prayer time integration.

## Features

- **Modern UI/UX** with Tailwind CSS
- **Responsive Design** for mobile and desktop
- **Real-time Prayer Times** integration
- **Task Management** with priority levels
- **Masjid Finder** and information
- **Daily Hadith** display
- **Server-Side Rendering** with Next.js App Router
- **Type-Safe** with TypeScript

## Tech Stack

- **Next.js 14.2** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **date-fns** - Date manipulation

## Prerequisites

- Node.js >= 20.0.0
- npm >= 10.0.0

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create a `.env.local` file in the frontend directory:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` with your configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_PRAYER_API_KEY=your_prayer_api_key
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

### 4. Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout component
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── Navbar.tsx        # Navigation component
│   └── TaskCard.tsx      # Task card component
├── lib/                  # Utility functions
├── public/               # Static assets
├── next.config.js        # Next.js configuration
├── tailwind.config.ts    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies and scripts
```

## Available Scripts

### Development

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm start            # Start production server
npm run lint         # Run ESLint
```

## Components

### Navbar

Navigation component with links to main sections:
- Home
- Tasks
- Masjids
- Daily Hadith

**Props**: None

### TaskCard

Displays individual task information with actions.

**Props**:
- `task` - Task object with details
- `onUpdate` - Callback for updating task
- `onDelete` - Callback for deleting task

## API Integration

The frontend connects to the FastAPI backend running at `http://localhost:8000/api/v1`

### Endpoints Used

- `GET /tasks` - Fetch all tasks
- `GET /tasks/{id}` - Fetch single task
- `POST /tasks` - Create new task
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `GET /masjids` - Fetch masjids
- `GET /hadith/today` - Fetch today's hadith

## Styling

This project uses Tailwind CSS for styling. The configuration includes:

- Custom color scheme
- Responsive breakpoints
- Dark mode support
- Custom utility classes

### Color Palette

- Primary: Indigo/Blue tones
- Background: Gradient from blue-50 to indigo-100
- Text: Gray scale
- Accents: Green for success, Red for priority

## Environment Variables

### Required

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000/api/v1)

### Optional

- `NEXT_PUBLIC_PRAYER_API_KEY` - API key for prayer times service
- `NEXT_PUBLIC_GOOGLE_MAPS_KEY` - Google Maps API key for masjid locations

## Development Guidelines

### Code Style

- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Implement proper error handling
- Add loading states for async operations

### Component Guidelines

- Keep components small and focused
- Use proper prop typing
- Implement proper accessibility (a11y)
- Add proper error boundaries
- Use client components ('use client') when needed

### State Management

- Use React hooks (useState, useEffect) for local state
- Consider Context API for global state if needed
- Implement proper data fetching patterns

## Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```bash
# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Build Errors

Clear Next.js cache:

```bash
rm -rf .next
npm run build
```

### Module Not Found

Reinstall dependencies:

```bash
rm -rf node_modules package-lock.json
npm install
```

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project to Vercel
3. Configure environment variables
4. Deploy

### Docker

```bash
docker build -t salaatflow-frontend .
docker run -p 3000:3000 salaatflow-frontend
```

### Manual Deployment

```bash
npm run build
# Copy .next, public, and package.json to server
npm install --production
npm start
```

## Performance Optimization

- Images are optimized with Next.js Image component
- CSS is purged in production
- Code splitting enabled by default
- Server-side rendering for better SEO
- Static generation where possible

## Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Screen reader friendly
- Color contrast compliance

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style
2. Write meaningful commit messages
3. Test thoroughly before submitting
4. Update documentation as needed

## License

MIT

## Support

For issues and questions:
- Check existing issues on GitHub
- Create new issue with detailed description
- Include error messages and screenshots

## Roadmap

- [ ] Add authentication and user management
- [ ] Implement real-time notifications
- [ ] Add offline support with PWA
- [ ] Integrate prayer time calculations
- [ ] Add task sharing capabilities
- [ ] Implement task templates
- [ ] Add calendar view
- [ ] Mobile app version
