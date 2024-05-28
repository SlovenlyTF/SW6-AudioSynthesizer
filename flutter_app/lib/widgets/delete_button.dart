import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_app/states/archive_delete_notifier.dart';
import 'package:provider/provider.dart';

class DeleteButton extends StatefulWidget {
  const DeleteButton({super.key, required this.index, required this.filePath, this.onDelete, this.size = 50});

  final int index;
  final String filePath;
  final VoidCallback? onDelete;
  final double size;

  @override
  _DeleteButtonState createState() => _DeleteButtonState();
}

class _DeleteButtonState extends State<DeleteButton> {
  @override
  Widget build(BuildContext context) {
    return Consumer<ArchiveDeleteNotifier>(
      builder: (context, archiveDeleteState, child) {
        bool isActive = archiveDeleteState.activeIndex == widget.index;
        return GestureDetector(
          onTap: () {
            // When pressing for the first time, open delete confirmation
            if (!isActive) {
              archiveDeleteState.setActiveIndex(widget.index);
              return;
            }
            
            // When pressing a second time, delete file
            _performDelete(widget.filePath);
            // Reset active index
            archiveDeleteState.setActiveIndex(-1);
          },
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            padding: const EdgeInsets.all(0),
            curve: Curves.easeInOut,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              color: isActive ? Colors.red : Colors.grey[400],
            ),
            width: isActive ? 120 : 44, // Change width based on isActive state
            height: 44,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center, // Align contents vertically
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                const Icon(Icons.delete, color: Colors.white),
                if (isActive) const SizedBox(width: 8),
                if (isActive) const Flexible(
                  child: Text(
                    'Delete?',
                    style: TextStyle(color: Colors.white),
                    overflow: TextOverflow.clip,
                    softWrap: false,
                  ),
                ),
              ],
            ),
          ),
        );
      }
    );
  }

  void _performDelete(String filePath) {
    // Perform delete action here
    try {
      File file = File(filePath);
      file.deleteSync();
      print('Deleted $filePath successfully!');
      if(widget.onDelete != null) widget.onDelete!();
    } catch (e) {
      print('Error deleting file: $e');
    }
  }
}