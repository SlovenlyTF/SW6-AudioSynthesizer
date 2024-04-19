import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

class ShareButton extends StatefulWidget {
  const ShareButton({super.key, required this.filePath, this.size = 75});

  final String filePath;
  final double size;

  @override
  State<ShareButton> createState() => _ShareButtonState();
}

class _ShareButtonState extends State<ShareButton> {

  Future<void> shareFile() async {
    // Get file and copy it to archive
    final result = await Share.shareXFiles([XFile(widget.filePath)],
    text: 'I generated this audio with Sonic Eye! 🧿');

    if (result.status == ShareResultStatus.success) {
      print('Thank you for sharing the audio :)');
    }
  }

  @override
  Widget build(BuildContext context) {  
    return GestureDetector(
      onTap: shareFile,
      child: Container(
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          color: Colors.green[500],
        ),
        child: const Icon(Icons.ios_share, color: Colors.white),
      ),
    );
  }
}
