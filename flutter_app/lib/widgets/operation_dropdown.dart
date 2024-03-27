import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:provider/provider.dart';

class OperationDropdown extends StatefulWidget {
  const OperationDropdown({super.key});

  @override
  State<OperationDropdown> createState() => _OperationDropdownState();
}

class _OperationDropdownState extends State<OperationDropdown> {

  final TextEditingController operationController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final generationOptions = Provider.of<GenerationOptionState>(context, listen: false);

    return  DropdownMenu<OperationLabel>(
      initialSelection: OperationLabel.flipAudio,
      controller: operationController,
      requestFocusOnTap: true,
      label: const Text('Operation', style: TextStyle(color: Colors.white)),
      textStyle: const TextStyle(
        color: Colors.white,
      ),
      trailingIcon: const Icon(
        Icons.arrow_drop_down,
        color: Colors.white,
      ),
      selectedTrailingIcon: const Icon(
        Icons.arrow_drop_up,
        color: Colors.white,
      ),
      onSelected: (OperationLabel? operation) {
        generationOptions.setOperation(operation ?? OperationLabel.flipAudio);
      },
      dropdownMenuEntries: OperationLabel.values
          .map<DropdownMenuEntry<OperationLabel>>(
              (OperationLabel operation) {
        return DropdownMenuEntry<OperationLabel>(
          value: operation,
          label: operation.label,
        );
      }).toList(),
    );
  }
}