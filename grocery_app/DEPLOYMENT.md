# FreshMart Grocery App - Deployment Guide

## 🚀 Quick Start

This Flutter Firebase grocery application is now ready for deployment! Follow these steps to get your app running.

## 📋 Prerequisites

- Flutter SDK 3.24.5+
- Dart SDK 3.5.4+
- Firebase CLI
- Android Studio / Xcode (for mobile development)
- Node.js (for Firebase CLI)

## 🔧 Setup Instructions

### 1. Firebase Configuration

#### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Enter project name: `freshmart-grocery` (or your preferred name)
4. Enable Google Analytics (optional)
5. Create project

#### Step 2: Enable Firebase Services
1. **Authentication**:
   - Go to Authentication > Sign-in method
   - Enable "Email/Password" provider
   - Optionally enable "Google" for social login

2. **Firestore Database**:
   - Go to Firestore Database
   - Create database in "production mode"
   - Choose location closest to your users

3. **Storage**:
   - Go to Storage
   - Get started with default rules
   - Choose same location as Firestore

4. **Cloud Messaging** (for push notifications):
   - Go to Cloud Messaging
   - No additional setup required initially

#### Step 3: Configure Flutter App
1. Install Firebase CLI:
   ```bash
   npm install -g firebase-tools
   ```

2. Login to Firebase:
   ```bash
   firebase login
   ```

3. Install FlutterFire CLI:
   ```bash
   dart pub global activate flutterfire_cli
   ```

4. Configure Firebase for your app:
   ```bash
   cd grocery_app
   flutterfire configure
   ```
   - Select your Firebase project
   - Choose platforms (iOS, Android, Web)
   - This will generate `firebase_options.dart` with your actual config

### 2. Local Development Setup

#### Step 1: Install Dependencies
```bash
cd grocery_app
flutter pub get
```

#### Step 2: Run the App
```bash
# For Android
flutter run

# For iOS (requires macOS and Xcode)
flutter run -d ios

# For web
flutter run -d chrome
```

### 3. Firebase Security Rules

#### Firestore Security Rules
Update your Firestore rules in Firebase Console:

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
      allow write: if false; // Only allow writes through admin panel
    }
    
    // Categories are readable by all authenticated users
    match /categories/{categoryId} {
      allow read: if request.auth != null;
      allow write: if false; // Only allow writes through admin panel
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
    
    // Reviews belong to users
    match /reviews/{reviewId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
  }
}
```

#### Storage Security Rules
Update your Storage rules in Firebase Console:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // User profile images
    match /users/{userId}/profile/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId
        && request.resource.size < 5 * 1024 * 1024; // 5MB limit
    }
    
    // Product images (read-only for users)
    match /products/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if false; // Only allow writes through admin panel
    }
  }
}
```

### 4. Sample Data Setup

#### Option 1: Manual Data Entry
1. Go to Firebase Console > Firestore Database
2. Create collections manually:
   - `categories` - Product categories
   - `products` - Product catalog
   - `users` - User profiles (created automatically on registration)

#### Option 2: Import Sample Data
Use the provided sample data in `assets/data/sample_products.json` to populate your database.

### 5. Environment Configuration

#### Create Environment File
Create a `.env` file in the root directory:
```env
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id

# Payment Gateway (Optional)
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret

# Other API Keys
GOOGLE_MAPS_API_KEY=your_google_maps_key
```

#### Update App Configuration
Update `lib/core/constants/app_constants.dart` with your specific configuration if needed.

### 6. Building for Production

#### Android
1. **Update App Configuration**:
   - Update `android/app/src/main/AndroidManifest.xml`
   - Update `android/app/build.gradle` with your signing config

2. **Build APK**:
   ```bash
   flutter build apk --release
   ```

3. **Build App Bundle** (recommended for Play Store):
   ```bash
   flutter build appbundle --release
   ```

#### iOS
1. **Update iOS Configuration**:
   - Open `ios/Runner.xcworkspace` in Xcode
   - Update Bundle Identifier
   - Configure signing certificates

2. **Build for iOS**:
   ```bash
   flutter build ios --release
   ```

#### Web
```bash
flutter build web --release
```

### 7. Deployment Options

#### Firebase Hosting (for Web)
```bash
# Build web version
flutter build web

# Initialize Firebase Hosting
firebase init hosting

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

#### App Stores
- **Google Play Store**: Upload the generated `.aab` file
- **Apple App Store**: Use Xcode to upload the iOS build

### 8. Testing

#### Run Tests
```bash
# Unit tests
flutter test

# Integration tests
flutter test integration_test/

# Widget tests
flutter test test/widget_test.dart
```

#### Manual Testing Checklist
- [ ] User registration and login
- [ ] Product browsing and search
- [ ] Cart functionality
- [ ] Order placement
- [ ] Profile management
- [ ] Offline functionality

### 9. Monitoring and Analytics

#### Firebase Analytics
- Already configured with Firebase initialization
- Custom events can be added for user behavior tracking

#### Crashlytics
Add Firebase Crashlytics for crash reporting:
```bash
flutter pub add firebase_crashlytics
```

### 10. Maintenance

#### Regular Updates
- Update Flutter SDK regularly
- Update Firebase packages
- Monitor Firebase usage and costs
- Update security rules as needed

#### Backup Strategy
- Enable Firestore automatic backups
- Regular export of user data
- Version control for app releases

## 🎯 Key Features Implemented

✅ **Authentication System**
- Email/Password registration and login
- Password reset functionality
- User profile management

✅ **Product Management**
- Product catalog with categories
- Search and filter functionality
- Product details with images

✅ **Shopping Cart**
- Add/remove items
- Quantity management
- Persistent cart storage

✅ **Order Management**
- Order placement
- Order history
- Order status tracking

✅ **Modern UI/UX**
- Material 3 design
- Dark/Light theme support
- Responsive design
- Smooth animations

✅ **State Management**
- Riverpod for efficient state management
- Reactive UI updates

✅ **Offline Support**
- Local data caching
- Offline cart functionality

## 📱 App Structure

```
lib/
├── core/                 # Core utilities and constants
├── data/                 # Data models and repositories
├── domain/               # Business logic
├── presentation/         # UI components and pages
├── services/             # Firebase and other services
└── main.dart            # App entry point
```

## 🛠️ Tech Stack

- **Frontend**: Flutter 3.24.5
- **Backend**: Firebase (Auth, Firestore, Storage, FCM)
- **State Management**: Riverpod
- **Local Storage**: SQLite, SharedPreferences
- **UI Framework**: Material 3
- **Architecture**: Clean Architecture

## 📞 Support

For support and questions:
- Check the [README.md](README.md) for detailed documentation
- Create issues in the repository
- Contact: support@freshmart.com

## 🔐 Security Notes

- Never commit Firebase configuration files to public repositories
- Use environment variables for sensitive data
- Regularly audit Firebase security rules
- Implement proper user input validation
- Use HTTPS for all network requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy Coding! 🚀**

Your FreshMart grocery app is now ready to serve customers with a modern, scalable, and robust grocery delivery experience!