class AppConstants {
  // App Info
  static const String appName = 'FreshMart';
  static const String appVersion = '1.0.0';
  
  // Firebase Collections
  static const String usersCollection = 'users';
  static const String productsCollection = 'products';
  static const String categoriesCollection = 'categories';
  static const String ordersCollection = 'orders';
  static const String cartCollection = 'cart';
  static const String addressesCollection = 'addresses';
  static const String reviewsCollection = 'reviews';
  static const String bannersCollection = 'banners';
  static const String couponsCollection = 'coupons';
  
  // SharedPreferences Keys
  static const String userIdKey = 'user_id';
  static const String userTokenKey = 'user_token';
  static const String themeKey = 'theme_key';
  static const String languageKey = 'language_key';
  static const String isFirstTimeKey = 'is_first_time';
  static const String cartItemsKey = 'cart_items';
  
  // API Endpoints (if using additional REST APIs)
  static const String baseUrl = 'https://api.freshmart.com/v1';
  static const String paymentBaseUrl = 'https://api.stripe.com/v1';
  
  // Image Paths
  static const String logoPath = 'assets/images/logo.png';
  static const String placeholderPath = 'assets/images/placeholder.png';
  static const String emptyCartPath = 'assets/images/empty_cart.png';
  static const String noInternetPath = 'assets/images/no_internet.png';
  
  // Animation Paths
  static const String loadingAnimation = 'assets/animations/loading.json';
  static const String successAnimation = 'assets/animations/success.json';
  static const String errorAnimation = 'assets/animations/error.json';
  
  // Dimensions
  static const double padding = 16.0;
  static const double margin = 16.0;
  static const double borderRadius = 12.0;
  static const double iconSize = 24.0;
  static const double buttonHeight = 48.0;
  static const double cardElevation = 4.0;
  
  // Durations
  static const Duration animationDuration = Duration(milliseconds: 300);
  static const Duration splashDuration = Duration(seconds: 3);
  static const Duration debounceDelay = Duration(milliseconds: 500);
  
  // Limits
  static const int maxCartItems = 99;
  static const int maxImageSize = 5 * 1024 * 1024; // 5MB
  static const int searchHistoryLimit = 10;
  static const int reviewCharacterLimit = 500;
  
  // Error Messages
  static const String networkError = 'Please check your internet connection';
  static const String unknownError = 'Something went wrong. Please try again';
  static const String authError = 'Authentication failed. Please login again';
  static const String permissionError = 'Permission denied';
  
  // Success Messages
  static const String orderPlaced = 'Order placed successfully!';
  static const String profileUpdated = 'Profile updated successfully!';
  static const String itemAddedToCart = 'Item added to cart';
  static const String itemRemovedFromCart = 'Item removed from cart';
  
  // Payment Methods
  static const String creditCard = 'Credit Card';
  static const String debitCard = 'Debit Card';
  static const String upi = 'UPI';
  static const String netBanking = 'Net Banking';
  static const String cashOnDelivery = 'Cash on Delivery';
  
  // Order Status
  static const String orderPending = 'pending';
  static const String orderConfirmed = 'confirmed';
  static const String orderProcessing = 'processing';
  static const String orderShipped = 'shipped';
  static const String orderDelivered = 'delivered';
  static const String orderCancelled = 'cancelled';
  
  // Product Categories
  static const List<String> mainCategories = [
    'Fruits & Vegetables',
    'Dairy & Bakery',
    'Meat & Seafood',
    'Beverages',
    'Snacks & Confectionery',
    'Personal Care',
    'Household',
    'Baby Care',
  ];
}

class AppStrings {
  // Auth
  static const String login = 'Login';
  static const String register = 'Register';
  static const String forgotPassword = 'Forgot Password?';
  static const String resetPassword = 'Reset Password';
  static const String logout = 'Logout';
  static const String email = 'Email';
  static const String password = 'Password';
  static const String confirmPassword = 'Confirm Password';
  static const String fullName = 'Full Name';
  static const String phoneNumber = 'Phone Number';
  
  // Home
  static const String home = 'Home';
  static const String search = 'Search';
  static const String categories = 'Categories';
  static const String featured = 'Featured Products';
  static const String bestSellers = 'Best Sellers';
  static const String deals = 'Today\'s Deals';
  
  // Product
  static const String products = 'Products';
  static const String productDetails = 'Product Details';
  static const String addToCart = 'Add to Cart';
  static const String buyNow = 'Buy Now';
  static const String quantity = 'Quantity';
  static const String price = 'Price';
  static const String description = 'Description';
  static const String reviews = 'Reviews';
  static const String rating = 'Rating';
  
  // Cart
  static const String cart = 'Cart';
  static const String emptyCart = 'Your cart is empty';
  static const String total = 'Total';
  static const String subtotal = 'Subtotal';
  static const String tax = 'Tax';
  static const String delivery = 'Delivery';
  static const String checkout = 'Checkout';
  
  // Orders
  static const String orders = 'Orders';
  static const String orderHistory = 'Order History';
  static const String orderDetails = 'Order Details';
  static const String trackOrder = 'Track Order';
  static const String reorder = 'Reorder';
  static const String cancelOrder = 'Cancel Order';
  
  // Profile
  static const String profile = 'Profile';
  static const String editProfile = 'Edit Profile';
  static const String addresses = 'Addresses';
  static const String paymentMethods = 'Payment Methods';
  static const String notifications = 'Notifications';
  static const String settings = 'Settings';
  static const String help = 'Help & Support';
  static const String about = 'About';
  
  // Common
  static const String save = 'Save';
  static const String cancel = 'Cancel';
  static const String delete = 'Delete';
  static const String edit = 'Edit';
  static const String add = 'Add';
  static const String remove = 'Remove';
  static const String update = 'Update';
  static const String loading = 'Loading...';
  static const String retry = 'Retry';
  static const String ok = 'OK';
  static const String yes = 'Yes';
  static const String no = 'No';
}