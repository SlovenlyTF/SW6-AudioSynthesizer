import 'package:flutter/foundation.dart';

// Maps label of operation to endpoint used in API URL
enum OperationLabel {
  flipAudio('Flip Audio', 'flip-audio', null),
  toSine('To Sine', 'to-sine', null),
  toPiano('To piano', 'to-midi', {'soundfont': 'piano.sf2'});

  const OperationLabel(this.label, this.endpoint, this.parameters);
  final String label;
  final String endpoint;
  final Map<String, String>? parameters;
}

class GenerationOptionState extends ChangeNotifier {
  OperationLabel operation = OperationLabel.flipAudio;

  OperationLabel get getOperation => operation;

  void setOperation(OperationLabel value) {
    operation = value;
    notifyListeners();
  }
}
