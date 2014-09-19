#!/bin/sh

rm Open311Map.wgt
cd Open311Map
zip -r ../Open311Map.wgt *
cd ..

rm Open311Info.wgt
cd Open311Info
zip -r ../Open311Info.wgt *
cd ..

rm Open311Image.wgt
cd Open311Image
zip -r ../Open311Image.wgt *
cd ..
