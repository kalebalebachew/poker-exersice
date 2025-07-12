FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies with npm install instead of npm ci
RUN npm install --legacy-peer-deps

# Copy the rest of the application
COPY . .

# Set environment variables
ENV NEXT_PUBLIC_API_URL=http://localhost:8000


# Build the application
RUN npm run build

# Expose the port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "start"] 