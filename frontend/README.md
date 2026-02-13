# Frontend - Next.js with TypeScript

Modern React frontend with TypeScript for the AI appointment chatbot.

## Features

- Next.js 14 with TypeScript
- Tailwind CSS for styling
- JWT authentication
- Real-time chat interface
- Responsive design
- Auto-scrolling chat messages
- Session management

## Setup

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your backend API URL

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

## Project Structure

```
src/
├── components/
│   ├── ChatWindow.tsx      # Main chat interface
│   └── Layout.tsx          # App layout wrapper
├── contexts/
│   └── AuthContext.tsx     # Authentication context
├── lib/
│   └── api.ts              # API client with interceptors
├── pages/
│   ├── _app.tsx            # App wrapper
│   ├── _document.tsx       # HTML document
│   ├── index.tsx           # Home page (chat)
│   ├── login.tsx           # Login page
│   └── register.tsx        # Registration page
└── styles/
    └── globals.css         # Global styles
```

## Pages

- `/` - Main chat interface (protected)
- `/login` - User login
- `/register` - User registration

## Demo Credentials

- Email: john.doe@example.com
- Password: password123

## Development

```bash
# Run development server
npm run dev

# Lint code
npm run lint

# Build for production
npm run build
```

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:4000
```

## Features

### Authentication
- JWT token management
- Auto token refresh
- Protected routes
- Logout functionality

### Chat Interface
- Real-time messaging
- Message history
- Auto-scroll to latest message
- Loading indicators
- Error handling

### UI/UX
- Clean, modern design
- Responsive layout
- Smooth animations
- Accessible components
