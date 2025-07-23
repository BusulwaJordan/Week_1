import 'package:cloud_firestore/cloud_firestore.dart';
import 'product_model.dart';

class CartItemModel {
  final String id;
  final String userId;
  final String productId;
  final ProductModel product;
  final int quantity;
  final double price; // Price at the time of adding to cart
  final DateTime addedAt;
  final DateTime updatedAt;

  CartItemModel({
    required this.id,
    required this.userId,
    required this.productId,
    required this.product,
    required this.quantity,
    required this.price,
    required this.addedAt,
    required this.updatedAt,
  });

  // Factory constructor from JSON
  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      id: json['id'] ?? '',
      userId: json['userId'] ?? '',
      productId: json['productId'] ?? '',
      product: ProductModel.fromJson(json['product']),
      quantity: json['quantity'] ?? 1,
      price: (json['price'] ?? 0.0).toDouble(),
      addedAt: json['addedAt'] is Timestamp
          ? (json['addedAt'] as Timestamp).toDate()
          : DateTime.parse(json['addedAt']),
      updatedAt: json['updatedAt'] is Timestamp
          ? (json['updatedAt'] as Timestamp).toDate()
          : DateTime.parse(json['updatedAt']),
    );
  }

  // Factory constructor from Firestore DocumentSnapshot
  factory CartItemModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return CartItemModel.fromJson({...data, 'id': doc.id});
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'productId': productId,
      'product': product.toJson(),
      'quantity': quantity,
      'price': price,
      'addedAt': Timestamp.fromDate(addedAt),
      'updatedAt': Timestamp.fromDate(updatedAt),
    };
  }

  // Convert to JSON for Firestore (without id)
  Map<String, dynamic> toFirestore() {
    final json = toJson();
    json.remove('id');
    return json;
  }

  // Calculate total price for this cart item
  double get totalPrice {
    return price * quantity;
  }

  // Check if quantity can be increased
  bool get canIncreaseQuantity {
    return quantity < product.stock;
  }

  // Check if quantity can be decreased
  bool get canDecreaseQuantity {
    return quantity > 1;
  }

  // Copy with method for immutability
  CartItemModel copyWith({
    String? id,
    String? userId,
    String? productId,
    ProductModel? product,
    int? quantity,
    double? price,
    DateTime? addedAt,
    DateTime? updatedAt,
  }) {
    return CartItemModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      productId: productId ?? this.productId,
      product: product ?? this.product,
      quantity: quantity ?? this.quantity,
      price: price ?? this.price,
      addedAt: addedAt ?? this.addedAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  String toString() {
    return 'CartItemModel(id: $id, userId: $userId, productId: $productId, product: $product, quantity: $quantity, price: $price, addedAt: $addedAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is CartItemModel &&
        other.id == id &&
        other.userId == userId &&
        other.productId == productId &&
        other.product == product &&
        other.quantity == quantity &&
        other.price == price &&
        other.addedAt == addedAt &&
        other.updatedAt == updatedAt;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        userId.hashCode ^
        productId.hashCode ^
        product.hashCode ^
        quantity.hashCode ^
        price.hashCode ^
        addedAt.hashCode ^
        updatedAt.hashCode;
  }
}