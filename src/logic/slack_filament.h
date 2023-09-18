/// @file slack_filament.h
#pragma once
#include "command_base.h"

namespace logic {

class SlackFilament : public CommandBase {
public:
    inline SlackFilament()
        : CommandBase() {}

    /// Restart the automaton
    /// @param param is not used, always unloads from the active slot
    bool Reset(uint8_t param) override;

    /// @returns true if the state machine finished its job, false otherwise
    bool StepInner() override;

private:
    /// Common code for a correct completion of SlackFilament
    void SlackFinishedCorrectly();
};

/// The one and only instance of SlackFilament state machine in the FW
extern SlackFilament slackFilament;


} // namespace logic
