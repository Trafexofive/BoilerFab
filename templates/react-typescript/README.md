# {{PROJECT_NAME}}

{{#if description}}{{description}}{{else}}A modern React application built with TypeScript and Vite.{{/if}}

## Features

- ⚡️ **Vite** for fast development and building
- ⚛️ **React 18** with TypeScript
{{#if (eq ui_library "tailwind")}}
- 🎨 **Tailwind CSS** for styling
{{/if}}
{{#if use_router}}
- 🧭 **React Router** for navigation
{{/if}}
{{#if (eq state_management "zustand")}}
- 🐻 **Zustand** for state management
{{/if}}
{{#if (eq state_management "redux")}}
- 🗃️ **Redux Toolkit** for state management
{{/if}}
- 📱 **Responsive design** ready
- 🔧 **ESLint** for code quality
- 🚀 **Production ready** build process

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm, yarn, or pnpm

### Installation

```bash
# Install dependencies
npm install
# or
yarn install
# or 
pnpm install
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:5173 in your browser
```

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Code Quality

```bash
# Run ESLint
npm run lint

# Type checking
npm run type-check
```

## Project Structure

```
{{PROJECT_NAME}}/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API services
│   ├── types/           # TypeScript type definitions
│   ├── utils/           # Utility functions
│   ├── App.tsx          # Main App component
│   ├── main.tsx         # Application entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
{{#if (eq ui_library "tailwind")}}
└── tailwind.config.js   # Tailwind CSS configuration
{{/if}}
```

## Available Scripts

- `dev` - Start development server
- `build` - Build for production
- `preview` - Preview production build locally
- `lint` - Run ESLint
- `type-check` - Run TypeScript compiler without emitting files

{{#if use_router}}
## Routing

This project uses React Router for navigation. Routes are defined in `App.tsx`:

- `/` - Home page
- `/about` - About page

Add new routes by importing your page components and adding them to the `Routes` component.
{{/if}}

{{#if (eq state_management "zustand")}}
## State Management

This project uses Zustand for state management. Create stores in the `src/stores/` directory and use them in your components with the `useStore` hook.
{{/if}}

{{#if (eq state_management "redux")}}
## State Management

This project uses Redux Toolkit for state management. Create slices in the `src/store/` directory and configure them in your store.
{{/if}}

## Styling

{{#if (eq ui_library "tailwind")}}
This project uses Tailwind CSS for styling. Utility classes are available throughout the application. Customize the design system in `tailwind.config.js`.

### Common Patterns

```tsx
// Button component
<button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
  Click me
</button>

// Card component
<div className="bg-white rounded-lg shadow-md p-6">
  <h2 className="text-xl font-semibold mb-4">Card Title</h2>
  <p className="text-gray-600">Card content</p>
</div>
```
{{else}}
Customize styles in your CSS files or add a UI library of your choice.
{{/if}}

## Deployment

### Netlify

```bash
# Build the project
npm run build

# Deploy the dist/ folder to Netlify
```

### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Static Hosting

The build output in `dist/` can be deployed to any static hosting service.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.