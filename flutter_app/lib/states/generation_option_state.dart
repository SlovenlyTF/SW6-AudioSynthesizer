import 'package:flutter/foundation.dart';

// Maps label of operation to endpoint used in API URL
enum OperationLabel {
  midiPiano('Piano', 'to-midi', {'soundfont': 'piano.sf2'}),
  midiViolin('Violin', 'to-midi', {'soundfont': 'violin.sf2'}),
  midiTuba('Tuba', 'to-midi', {'soundfont': 'tuba.sf2'}),
  midiHurdyGurdy('Hurdy gurdy', 'to-midi', {'soundfont': 'hurdy_gurdy.sf2'}),
  midiFemaleVocal('Female vocal', 'to-midi', {'soundfont': 'female_vocalizer.sf2'}),
  midiZombie('Zombie', 'to-midi', {'soundfont': 'zombie.sf2'}),
  midiVista('Windows vista', 'to-midi', {'soundfont': 'vista.sf2'});

  const OperationLabel(this.label, this.endpoint, this.parameters);
  final String label;
  final String endpoint;
  final Map<String, String>? parameters;
}

class GenerationOptionState extends ChangeNotifier {
  OperationLabel operation = OperationLabel.midiPiano;

  OperationLabel get getOperation => operation;

  void setOperation(OperationLabel value) {
    operation = value;
    notifyListeners();
  }
}
