import 'package:flutter/material.dart';
import 'package:flutter_app/states/archive_player_notifier.dart';
import 'package:flutter_app/widgets/audio_controller.dart';
import 'package:just_audio/just_audio.dart';
import 'package:provider/provider.dart';

class ArchiveAudioController extends StatefulWidget {
  const ArchiveAudioController({super.key, required this.index, required this.filePath, required this.playerTitle, this.canPlay});

  final int index;
  final Future<String> filePath;
  final Future<String> playerTitle;
  final bool? canPlay;

  @override
  State<ArchiveAudioController> createState() => _ArchiveAudioControllerState();
}


class _ArchiveAudioControllerState extends State<ArchiveAudioController> {
  late AudioPlayer _audioPlayer;
  bool _audioPlayerCreated = false;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ArchivePlayerNotifier>(
      builder: (context, archivePlayerState, child) {
        if (_audioPlayerCreated) {
          _audioPlayer.load();

          if(archivePlayerState.activeIndex != widget.index) {
            _audioPlayer.pause();
          }
        }

        return SizedBox(
          height: 100,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(left: 10, top: 3),
                child: FutureBuilder<String>(
                  future: widget.playerTitle,
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      return Text(snapshot.data!, style: const TextStyle(color: Colors.white, fontSize: 17));
                    } else {
                      return const Text('Audio File', style: TextStyle(color: Colors.white, fontSize: 17));
                    }
                  },
                ),
              ),
              
              AudioController(
                filePath: widget.filePath,
                canPlay: true, //ass for now
                onAudioPlayerCreated: (audioPlayer) {
                  setState(() {
                    _audioPlayer = audioPlayer;
                    _audioPlayerCreated = true; // Set the flag to true after the audio player is created
                  });
                },
                onPlayPause: (isPlaying) {
                  int newIndex = isPlaying ? widget.index : -1; 
                  archivePlayerState.setActiveIndex(newIndex);
                }
              ),
            ],
          ),
        );
    });
  }
}
