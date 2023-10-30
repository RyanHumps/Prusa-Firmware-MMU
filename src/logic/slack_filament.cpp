/// @file slack_filament.cpp
#include "slack_filament.h"
#include "../modules/globals.h"
#include "../modules/idler.h"
#include "../modules/motion.h"
#include "../modules/pulley.h"
#include "../debug.h"

namespace logic {

SlackFilament slackFilament;

bool SlackFilament::Reset(uint8_t /*param*/) {
    if (mg::globals.FilamentLoaded() < mg::FilamentLoadState::AtPulley) {
        return false; // avoid starting slackfilament if none is loaded to bondtech
    }
    state = ProgressCode::EngagingIdler;
    error = ErrorCode::RUNNING;
    mi::idler.Engage(mg::globals.ActiveSlot());
    return true;
}

void logic::SlackFilament::SlackFinishedCorrectly() {
    FinishedOK();
    mi::idler.Disengage();
}

bool SlackFilament::StepInner() {
    switch (state) {
    case ProgressCode::EngagingIdler:
        if (mi::idler.Engaged()) {
            state = ProgressCode::SlackingFilament;
            mpu::pulley.InitAxis();
            // fast feed in millimeters - if the EEPROM value is incorrect, we'll get the default length
                mg::globals.PulleyLoadFeedrate_mm_s() / 2,
            mpu::pulley.PlanMove(config::slackLength,
                mg::globals.PulleySlowFeedrate_mm_s());
        }
        return false;
    case ProgressCode::SlackingFilament:
        if (mm::motion.PlannedMoves(mm::Pulley) == 0) {
            SlackFinishedCorrectly();
        }
        return false;
    case ProgressCode::OK:
        return true;
    default: // we got into an unhandled state, better report it
        state = ProgressCode::ERRInternal;
        error = ErrorCode::INTERNAL;
        return true;
    }
    return false;
}

} // namespace logic
