# Historical estimate and entered-data audit
**ILLUSTRATIVE PERFORMANCE ESTIMATE.** Input constants and exponent were assumptions in a historical script and have not been independently validated against flight logs.

The preserved Python source uses 3400 g as assumed aggregate thrust, 1100 g baseline mass and seven minutes baseline time. Its 1.3-exponent relation is a power law, despite the original comment calling it exponential decay. The plotted weight/thrust percentage is a mass-equivalent ratio, not a measured or calibrated throttle command. The script was executed with a noninteractive plotting backend solely to check execution; that does not validate its constants, model or predicted endurance.

The original ODS was parsed independently from its XML. The transcription contains all 37 populated cells with row, column, literal text, stored value and value type. It preserves the archive, not a new experiment. Nine entries appear in the sheet, but no instrument model, setup, timestamped acquisition chain, specimen identity, uncertainty or raw logger samples were recovered. No new measured-thrust or endurance claim is inferred.

See data/archived_thrust_sheet_transcription.csv and the source/release hashes in data/included_original_assets.csv. Both original files remain untouched in evidence/original. The limits of the 19/20 retrospective composite statement remain separate from this estimate.
