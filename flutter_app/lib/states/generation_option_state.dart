import 'package:flutter/foundation.dart';

// Maps label of operation to endpoint used in API URL
enum OperationLabel {
  flipAudio('Flip Audio', 'flip-audio'),
  toSine('To Sine', 'to-sine');

  const OperationLabel(this.label, this.endpoint);
  final String label;
  final String endpoint;
}

class GenerationOptionState extends ChangeNotifier {
  OperationLabel operation = OperationLabel.flipAudio;

  OperationLabel get getOperation => operation;

  void setOperation(OperationLabel value) {
    operation = value;
    notifyListeners();
  }
}
