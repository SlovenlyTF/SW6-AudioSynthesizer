import 'package:flutter/foundation.dart';

class ArchiveDeleteNotifier extends ChangeNotifier {
  int _activeIndex = -1;
  int get activeIndex => _activeIndex;

  void setActiveIndex(int value) {
    _activeIndex = value;
    notifyListeners();
  }
}