import 'package:cloud_firestore/cloud_firestore.dart';

class ProductModel {
  final String id;
  final String name;
  final String description;
  final double price;
  final double? originalPrice;
  final String categoryId;
  final String categoryName;
  final List<String> images;
  final String unit; // kg, grams, liters, pieces, etc.
  final double unitValue; // 1.0, 500.0, etc.
  final int stock;
  final bool isAvailable;
  final bool isFeatured;
  final bool isOrganic;
  final double rating;
  final int reviewCount;
  final Map<String, dynamic>? nutritionInfo;
  final List<String> tags;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String? brand;
  final String? origin;
  final DateTime? expiryDate;
  final int? discount; // percentage

  ProductModel({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    this.originalPrice,
    required this.categoryId,
    required this.categoryName,
    this.images = const [],
    required this.unit,
    required this.unitValue,
    this.stock = 0,
    this.isAvailable = true,
    this.isFeatured = false,
    this.isOrganic = false,
    this.rating = 0.0,
    this.reviewCount = 0,
    this.nutritionInfo,
    this.tags = const [],
    required this.createdAt,
    required this.updatedAt,
    this.brand,
    this.origin,
    this.expiryDate,
    this.discount,
  });

  // Factory constructor from JSON
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      price: (json['price'] ?? 0.0).toDouble(),
      originalPrice: json['originalPrice']?.toDouble(),
      categoryId: json['categoryId'] ?? '',
      categoryName: json['categoryName'] ?? '',
      images: List<String>.from(json['images'] ?? []),
      unit: json['unit'] ?? 'pieces',
      unitValue: (json['unitValue'] ?? 1.0).toDouble(),
      stock: json['stock'] ?? 0,
      isAvailable: json['isAvailable'] ?? true,
      isFeatured: json['isFeatured'] ?? false,
      isOrganic: json['isOrganic'] ?? false,
      rating: (json['rating'] ?? 0.0).toDouble(),
      reviewCount: json['reviewCount'] ?? 0,
      nutritionInfo: json['nutritionInfo'],
      tags: List<String>.from(json['tags'] ?? []),
      createdAt: json['createdAt'] is Timestamp
          ? (json['createdAt'] as Timestamp).toDate()
          : DateTime.parse(json['createdAt']),
      updatedAt: json['updatedAt'] is Timestamp
          ? (json['updatedAt'] as Timestamp).toDate()
          : DateTime.parse(json['updatedAt']),
      brand: json['brand'],
      origin: json['origin'],
      expiryDate: json['expiryDate'] is Timestamp
          ? (json['expiryDate'] as Timestamp).toDate()
          : (json['expiryDate'] != null ? DateTime.parse(json['expiryDate']) : null),
      discount: json['discount'],
    );
  }

  // Factory constructor from Firestore DocumentSnapshot
  factory ProductModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return ProductModel.fromJson({...data, 'id': doc.id});
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'originalPrice': originalPrice,
      'categoryId': categoryId,
      'categoryName': categoryName,
      'images': images,
      'unit': unit,
      'unitValue': unitValue,
      'stock': stock,
      'isAvailable': isAvailable,
      'isFeatured': isFeatured,
      'isOrganic': isOrganic,
      'rating': rating,
      'reviewCount': reviewCount,
      'nutritionInfo': nutritionInfo,
      'tags': tags,
      'createdAt': Timestamp.fromDate(createdAt),
      'updatedAt': Timestamp.fromDate(updatedAt),
      'brand': brand,
      'origin': origin,
      'expiryDate': expiryDate != null ? Timestamp.fromDate(expiryDate!) : null,
      'discount': discount,
    };
  }

  // Convert to JSON for Firestore (without id)
  Map<String, dynamic> toFirestore() {
    final json = toJson();
    json.remove('id');
    return json;
  }

  // Calculate discounted price
  double get discountedPrice {
    if (discount != null && discount! > 0) {
      return price * (1 - discount! / 100);
    }
    return price;
  }

  // Get primary image
  String get primaryImage {
    return images.isNotEmpty ? images.first : '';
  }

  // Check if product is on sale
  bool get isOnSale {
    return discount != null && discount! > 0;
  }

  // Get formatted unit display
  String get unitDisplay {
    if (unitValue == 1.0) {
      return unit;
    }
    return '${unitValue.toStringAsFixed(unitValue.truncateToDouble() == unitValue ? 0 : 1)} $unit';
  }

  // Check if product is in stock
  bool get inStock {
    return stock > 0 && isAvailable;
  }

  // Copy with method for immutability
  ProductModel copyWith({
    String? id,
    String? name,
    String? description,
    double? price,
    double? originalPrice,
    String? categoryId,
    String? categoryName,
    List<String>? images,
    String? unit,
    double? unitValue,
    int? stock,
    bool? isAvailable,
    bool? isFeatured,
    bool? isOrganic,
    double? rating,
    int? reviewCount,
    Map<String, dynamic>? nutritionInfo,
    List<String>? tags,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? brand,
    String? origin,
    DateTime? expiryDate,
    int? discount,
  }) {
    return ProductModel(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      price: price ?? this.price,
      originalPrice: originalPrice ?? this.originalPrice,
      categoryId: categoryId ?? this.categoryId,
      categoryName: categoryName ?? this.categoryName,
      images: images ?? this.images,
      unit: unit ?? this.unit,
      unitValue: unitValue ?? this.unitValue,
      stock: stock ?? this.stock,
      isAvailable: isAvailable ?? this.isAvailable,
      isFeatured: isFeatured ?? this.isFeatured,
      isOrganic: isOrganic ?? this.isOrganic,
      rating: rating ?? this.rating,
      reviewCount: reviewCount ?? this.reviewCount,
      nutritionInfo: nutritionInfo ?? this.nutritionInfo,
      tags: tags ?? this.tags,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      brand: brand ?? this.brand,
      origin: origin ?? this.origin,
      expiryDate: expiryDate ?? this.expiryDate,
      discount: discount ?? this.discount,
    );
  }

  @override
  String toString() {
    return 'ProductModel(id: $id, name: $name, description: $description, price: $price, originalPrice: $originalPrice, categoryId: $categoryId, categoryName: $categoryName, images: $images, unit: $unit, unitValue: $unitValue, stock: $stock, isAvailable: $isAvailable, isFeatured: $isFeatured, isOrganic: $isOrganic, rating: $rating, reviewCount: $reviewCount, nutritionInfo: $nutritionInfo, tags: $tags, createdAt: $createdAt, updatedAt: $updatedAt, brand: $brand, origin: $origin, expiryDate: $expiryDate, discount: $discount)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is ProductModel &&
        other.id == id &&
        other.name == name &&
        other.description == description &&
        other.price == price &&
        other.originalPrice == originalPrice &&
        other.categoryId == categoryId &&
        other.categoryName == categoryName &&
        other.images == images &&
        other.unit == unit &&
        other.unitValue == unitValue &&
        other.stock == stock &&
        other.isAvailable == isAvailable &&
        other.isFeatured == isFeatured &&
        other.isOrganic == isOrganic &&
        other.rating == rating &&
        other.reviewCount == reviewCount &&
        other.nutritionInfo == nutritionInfo &&
        other.tags == tags &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt &&
        other.brand == brand &&
        other.origin == origin &&
        other.expiryDate == expiryDate &&
        other.discount == discount;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        name.hashCode ^
        description.hashCode ^
        price.hashCode ^
        originalPrice.hashCode ^
        categoryId.hashCode ^
        categoryName.hashCode ^
        images.hashCode ^
        unit.hashCode ^
        unitValue.hashCode ^
        stock.hashCode ^
        isAvailable.hashCode ^
        isFeatured.hashCode ^
        isOrganic.hashCode ^
        rating.hashCode ^
        reviewCount.hashCode ^
        nutritionInfo.hashCode ^
        tags.hashCode ^
        createdAt.hashCode ^
        updatedAt.hashCode ^
        brand.hashCode ^
        origin.hashCode ^
        expiryDate.hashCode ^
        discount.hashCode;
  }
}