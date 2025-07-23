import 'package:cloud_firestore/cloud_firestore.dart';
import 'cart_item_model.dart';

class OrderModel {
  final String id;
  final String userId;
  final String orderNumber;
  final List<CartItemModel> items;
  final double subtotal;
  final double tax;
  final double deliveryFee;
  final double discount;
  final double total;
  final String status; // pending, confirmed, processing, shipped, delivered, cancelled
  final String paymentMethod;
  final String paymentStatus; // pending, paid, failed, refunded
  final String? paymentId;
  final Map<String, dynamic> deliveryAddress;
  final DateTime? estimatedDeliveryDate;
  final DateTime? actualDeliveryDate;
  final String? trackingNumber;
  final String? notes;
  final DateTime createdAt;
  final DateTime updatedAt;
  final List<OrderStatusUpdate> statusHistory;

  OrderModel({
    required this.id,
    required this.userId,
    required this.orderNumber,
    required this.items,
    required this.subtotal,
    required this.tax,
    required this.deliveryFee,
    required this.discount,
    required this.total,
    required this.status,
    required this.paymentMethod,
    required this.paymentStatus,
    this.paymentId,
    required this.deliveryAddress,
    this.estimatedDeliveryDate,
    this.actualDeliveryDate,
    this.trackingNumber,
    this.notes,
    required this.createdAt,
    required this.updatedAt,
    this.statusHistory = const [],
  });

  // Factory constructor from JSON
  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'] ?? '',
      userId: json['userId'] ?? '',
      orderNumber: json['orderNumber'] ?? '',
      items: (json['items'] as List<dynamic>?)
          ?.map((item) => CartItemModel.fromJson(item))
          .toList() ?? [],
      subtotal: (json['subtotal'] ?? 0.0).toDouble(),
      tax: (json['tax'] ?? 0.0).toDouble(),
      deliveryFee: (json['deliveryFee'] ?? 0.0).toDouble(),
      discount: (json['discount'] ?? 0.0).toDouble(),
      total: (json['total'] ?? 0.0).toDouble(),
      status: json['status'] ?? 'pending',
      paymentMethod: json['paymentMethod'] ?? '',
      paymentStatus: json['paymentStatus'] ?? 'pending',
      paymentId: json['paymentId'],
      deliveryAddress: json['deliveryAddress'] ?? {},
      estimatedDeliveryDate: json['estimatedDeliveryDate'] is Timestamp
          ? (json['estimatedDeliveryDate'] as Timestamp).toDate()
          : (json['estimatedDeliveryDate'] != null ? DateTime.parse(json['estimatedDeliveryDate']) : null),
      actualDeliveryDate: json['actualDeliveryDate'] is Timestamp
          ? (json['actualDeliveryDate'] as Timestamp).toDate()
          : (json['actualDeliveryDate'] != null ? DateTime.parse(json['actualDeliveryDate']) : null),
      trackingNumber: json['trackingNumber'],
      notes: json['notes'],
      createdAt: json['createdAt'] is Timestamp
          ? (json['createdAt'] as Timestamp).toDate()
          : DateTime.parse(json['createdAt']),
      updatedAt: json['updatedAt'] is Timestamp
          ? (json['updatedAt'] as Timestamp).toDate()
          : DateTime.parse(json['updatedAt']),
      statusHistory: (json['statusHistory'] as List<dynamic>?)
          ?.map((status) => OrderStatusUpdate.fromJson(status))
          .toList() ?? [],
    );
  }

  // Factory constructor from Firestore DocumentSnapshot
  factory OrderModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return OrderModel.fromJson({...data, 'id': doc.id});
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'orderNumber': orderNumber,
      'items': items.map((item) => item.toJson()).toList(),
      'subtotal': subtotal,
      'tax': tax,
      'deliveryFee': deliveryFee,
      'discount': discount,
      'total': total,
      'status': status,
      'paymentMethod': paymentMethod,
      'paymentStatus': paymentStatus,
      'paymentId': paymentId,
      'deliveryAddress': deliveryAddress,
      'estimatedDeliveryDate': estimatedDeliveryDate != null 
          ? Timestamp.fromDate(estimatedDeliveryDate!) : null,
      'actualDeliveryDate': actualDeliveryDate != null 
          ? Timestamp.fromDate(actualDeliveryDate!) : null,
      'trackingNumber': trackingNumber,
      'notes': notes,
      'createdAt': Timestamp.fromDate(createdAt),
      'updatedAt': Timestamp.fromDate(updatedAt),
      'statusHistory': statusHistory.map((status) => status.toJson()).toList(),
    };
  }

  // Convert to JSON for Firestore (without id)
  Map<String, dynamic> toFirestore() {
    final json = toJson();
    json.remove('id');
    return json;
  }

  // Get total item count
  int get totalItems {
    return items.fold(0, (total, item) => total + item.quantity);
  }

  // Check if order can be cancelled
  bool get canBeCancelled {
    return status == 'pending' || status == 'confirmed';
  }

  // Check if order is completed
  bool get isCompleted {
    return status == 'delivered';
  }

  // Check if order is active (not cancelled or delivered)
  bool get isActive {
    return status != 'cancelled' && status != 'delivered';
  }

  // Get status color for UI
  String get statusColor {
    switch (status) {
      case 'pending':
        return '#FFA726';
      case 'confirmed':
        return '#42A5F5';
      case 'processing':
        return '#AB47BC';
      case 'shipped':
        return '#5C6BC0';
      case 'delivered':
        return '#66BB6A';
      case 'cancelled':
        return '#EF5350';
      default:
        return '#9E9E9E';
    }
  }

  // Copy with method for immutability
  OrderModel copyWith({
    String? id,
    String? userId,
    String? orderNumber,
    List<CartItemModel>? items,
    double? subtotal,
    double? tax,
    double? deliveryFee,
    double? discount,
    double? total,
    String? status,
    String? paymentMethod,
    String? paymentStatus,
    String? paymentId,
    Map<String, dynamic>? deliveryAddress,
    DateTime? estimatedDeliveryDate,
    DateTime? actualDeliveryDate,
    String? trackingNumber,
    String? notes,
    DateTime? createdAt,
    DateTime? updatedAt,
    List<OrderStatusUpdate>? statusHistory,
  }) {
    return OrderModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      orderNumber: orderNumber ?? this.orderNumber,
      items: items ?? this.items,
      subtotal: subtotal ?? this.subtotal,
      tax: tax ?? this.tax,
      deliveryFee: deliveryFee ?? this.deliveryFee,
      discount: discount ?? this.discount,
      total: total ?? this.total,
      status: status ?? this.status,
      paymentMethod: paymentMethod ?? this.paymentMethod,
      paymentStatus: paymentStatus ?? this.paymentStatus,
      paymentId: paymentId ?? this.paymentId,
      deliveryAddress: deliveryAddress ?? this.deliveryAddress,
      estimatedDeliveryDate: estimatedDeliveryDate ?? this.estimatedDeliveryDate,
      actualDeliveryDate: actualDeliveryDate ?? this.actualDeliveryDate,
      trackingNumber: trackingNumber ?? this.trackingNumber,
      notes: notes ?? this.notes,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      statusHistory: statusHistory ?? this.statusHistory,
    );
  }

  @override
  String toString() {
    return 'OrderModel(id: $id, userId: $userId, orderNumber: $orderNumber, items: $items, subtotal: $subtotal, tax: $tax, deliveryFee: $deliveryFee, discount: $discount, total: $total, status: $status, paymentMethod: $paymentMethod, paymentStatus: $paymentStatus, paymentId: $paymentId, deliveryAddress: $deliveryAddress, estimatedDeliveryDate: $estimatedDeliveryDate, actualDeliveryDate: $actualDeliveryDate, trackingNumber: $trackingNumber, notes: $notes, createdAt: $createdAt, updatedAt: $updatedAt, statusHistory: $statusHistory)';
  }
}

class OrderStatusUpdate {
  final String status;
  final String? message;
  final DateTime timestamp;

  OrderStatusUpdate({
    required this.status,
    this.message,
    required this.timestamp,
  });

  factory OrderStatusUpdate.fromJson(Map<String, dynamic> json) {
    return OrderStatusUpdate(
      status: json['status'] ?? '',
      message: json['message'],
      timestamp: json['timestamp'] is Timestamp
          ? (json['timestamp'] as Timestamp).toDate()
          : DateTime.parse(json['timestamp']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'message': message,
      'timestamp': Timestamp.fromDate(timestamp),
    };
  }

  @override
  String toString() {
    return 'OrderStatusUpdate(status: $status, message: $message, timestamp: $timestamp)';
  }
}