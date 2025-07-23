# FreshMart - Flutter Firebase Grocery App

A robust Flutter mobile application for grocery delivery with Firebase backend integration.

## Features

- **Authentication**: User registration, login, password reset, email verification
- **Product Catalog**: Browse products by categories, search, filters
- **Shopping Cart**: Add/remove items, quantity management
- **Order Management**: Place orders, track delivery, order history
- **User Profile**: Manage addresses, payment methods, preferences
- **Real-time Updates**: Live inventory updates, order status tracking
- **Modern UI**: Clean, responsive design with animations
- **State Management**: Riverpod for efficient state management
- **Offline Support**: Local database for offline functionality

## Tech Stack

- **Frontend**: Flutter 3.24.5
- **Backend**: Firebase (Auth, Firestore, Storage, Messaging)
- **State Management**: Riverpod
- **Local Database**: SQLite
- **UI Components**: Custom widgets with Material 3 design
- **Authentication**: Firebase Auth
- **Storage**: Firebase Storage for images
- **Push Notifications**: Firebase Cloud Messaging

## Getting Started

### Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK (>=3.0.0)
- Android Studio / VS Code
- Firebase CLI
- Android/iOS development environment

### Firebase Setup

1. **Create a Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Google Analytics (optional)

2. **Enable Firebase Services**
   - **Authentication**: Enable Email/Password provider
   - **Firestore Database**: Create database in production mode
   - **Storage**: Set up Firebase Storage
   - **Cloud Messaging**: Enable for push notifications

3. **Add Firebase to Your App**
   ```bash
   # Install Firebase CLI
   npm install -g firebase-tools
   
   # Login to Firebase
   firebase login
   
   # Initialize Firebase in your project
   firebase init
   ```

4. **Download Configuration Files**
   - Download `google-services.json` for Android
   - Download `GoogleService-Info.plist` for iOS
   - Place them in the appropriate directories:
     - Android: `android/app/google-services.json`
     - iOS: `ios/Runner/GoogleService-Info.plist`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd grocery_app
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Configure Firebase**
   - Add your Firebase configuration files as mentioned above
   - Update Firebase project settings if needed

4. **Run the app**
   ```bash
   # For Android
   flutter run

   # For iOS
   flutter run -d ios
   ```

## Project Structure

```
lib/
├── core/
│   ├── constants/          # App constants and strings
│   ├── theme/             # App theme and styling
│   ├── utils/             # Utility functions
│   ├── errors/            # Error handling
│   └── network/           # Network configurations
├── data/
│   ├── models/            # Data models
│   ├── repositories/      # Repository implementations
│   └── datasources/       # Data sources (local/remote)
├── domain/
│   ├── entities/          # Business entities
│   ├── repositories/      # Repository interfaces
│   └── usecases/          # Business logic
├── presentation/
│   ├── pages/             # UI screens
│   ├── widgets/           # Reusable widgets
│   └── providers/         # State management
├── services/
│   ├── firebase/          # Firebase services
│   ├── auth/              # Authentication services
│   ├── storage/           # Storage services
│   └── notification/      # Notification services
└── main.dart              # App entry point
```

## Key Features Implementation

### Authentication Flow
- Splash screen with app initialization
- Login/Register with email validation
- Password reset functionality
- Email verification
- Auto-login for authenticated users

### Product Management
- Product catalog with categories
- Search and filter functionality
- Product details with images
- Inventory management
- Price and discount handling

### Shopping Cart
- Add/remove items
- Quantity management
- Real-time price calculation
- Persistent cart storage

### Order Processing
- Checkout flow
- Address selection
- Payment integration
- Order tracking
- Status updates

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_API_KEY=your_api_key
STRIPE_PUBLISHABLE_KEY=your_stripe_key
```

### Firebase Security Rules

**Firestore Rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Products are readable by all authenticated users
    match /products/{productId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    // Orders belong to users
    match /orders/{orderId} {
      allow read, write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
    
    // Cart items belong to users
    match /cart/{cartId} {
      allow read, write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
  }
}
```

**Storage Rules:**
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /products/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        firestore.get(/databases/(default)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
  }
}
```

## Testing

```bash
# Run unit tests
flutter test

# Run integration tests
flutter test integration_test/

# Run tests with coverage
flutter test --coverage
```

## Building for Production

### Android
```bash
# Build APK
flutter build apk --release

# Build App Bundle (recommended for Play Store)
flutter build appbundle --release
```

### iOS
```bash
# Build for iOS
flutter build ios --release
```

## Deployment

### Firebase Hosting (for web version)
```bash
# Build web version
flutter build web

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

### App Stores
- Follow Flutter's official guide for publishing to [Google Play Store](https://docs.flutter.dev/deployment/android) and [Apple App Store](https://docs.flutter.dev/deployment/ios)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Architecture

This app follows Clean Architecture principles:
- **Presentation Layer**: UI components and state management
- **Domain Layer**: Business logic and entities
- **Data Layer**: Data sources and repositories

## State Management

Using Riverpod for:
- Authentication state
- Shopping cart state
- Product catalog state
- User preferences
- Loading states

## Libraries Used

- `firebase_core`: Firebase core functionality
- `firebase_auth`: Authentication
- `cloud_firestore`: NoSQL database
- `firebase_storage`: File storage
- `firebase_messaging`: Push notifications
- `flutter_riverpod`: State management
- `cached_network_image`: Image caching
- `shimmer`: Loading animations
- `lottie`: Vector animations
- `shared_preferences`: Local storage
- `sqflite`: Local database
- `form_field_validator`: Form validation
- `image_picker`: Image selection
- `geolocator`: Location services

## Support

For support, email support@freshmart.com or join our Slack channel.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flutter team for the amazing framework
- Firebase team for the backend services
- Material Design team for the design system
- Contributors and the open-source community
