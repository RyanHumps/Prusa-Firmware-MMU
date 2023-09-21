# Prusa-Firmware-MMU-Private

The purpose of this fork is to enble the MMU to act as a filament slacker. With the original firmware, the MMU is dormant during printing, and the extruder has the sole responsibility of pulling filament. Depending on the filament setup, this filament tension can tranlate significant motion to the print head, E-axis, and X-axis, particularly during long or rapid X-axis movements.

A `Ts` g-code is added to the [firmware](https://github.com/prusa3d/Prusa-Firmware) which will trigger the MMU idler to engage on the active material slot and run the pulley for the slacking amount defined in the [configuration](./src/config/config.h). It would be unsafe to keep the idler engaged for the entire print, so the each call of `Tr` will disengage the idler after the pulley is finished.

For extra filament to be slacked between the MMU and extruder, the original PTFE tube linking the two must be disconnected. Therefore, all other MMU functionality is lost. Filament must be manually guided into the extruder.

In theory, all of the original MMU functionality can be gained back by having a stationary filament load point. During a tool change, the extruder will make the appropriate move a pre-defined coordinate, close to the top of the printer frame, and "catch" the filament being fed to it, then return to the print. The extruder body's filament intake hole will need some sort of mating interface with the stationary filament feeding outlet. Some inspiration can probably be gained from mid-air jet refuling procedures.

A post processor is included, which can be referenced in PrusaSlicer and will add `Ts` calls throughout the exported g-code. It sums the filament consumed by any `G1 E` movement, and adds `Ts` to slack enough filament to replenish the consumption, thus always keeping the filament slacked, but not out of control, so long as it had sufficient slack to begin with when manually loaded. 

## How to prepare build env and tools
Run `./utils/bootstrap.py`

`bootstrap.py` will now download all the "missing" dependencies into the `.dependencies` folder:
- clang-format-9.0.0-noext
- cmake-3.22.5
- ninja-1.10.2
- avr-gcc-7.3.0

## How to build the preliminary project so far:
Now the process is the same as in the Buddy Firmware:
```
./utils/build.py
```

builds the firmware.hex in build/mmu_release

In case you'd like to build the project directly via cmake you can use an approach like this:
```
mkdir build
cd build
cmake .. -G Ninja -DCMAKE_TOOLCHAIN_FILE=../cmake/AvrGcc.cmake
ninja
```

It will produce a `MMU2SR_<version>.hex` file.
