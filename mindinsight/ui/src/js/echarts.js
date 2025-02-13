/**
 * Copyright 2021 Huawei Technologies Co., Ltd.All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import {useEChartsTheme} from './useEChartsTheme';

const echarts = require('echarts/lib/echarts');

const themeIndex = localStorage.getItem('miTheme') ?? '0';

export const echartsThemeName = 'MI_ECHARTS_THEME';

// Register echarts theme
echarts.registerTheme(echartsThemeName, useEChartsTheme(themeIndex));

import {
  LineChart,
  BarChart,
  PieChart,
  ParallelChart,
  RadarChart,
  CustomChart,
  ScatterChart,
  SankeyChart,
} from 'echarts/charts';

import {
  GridComponent,
  LegendComponent,
  TooltipComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
} from 'echarts/components';

echarts.use([
  LineChart,
  BarChart,
  PieChart,
  ParallelChart,
  RadarChart,
  CustomChart,
  ScatterChart,
  SankeyChart,
  GridComponent,
  LegendComponent,
  TooltipComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent,
  MarkPointComponent,
  MarkLineComponent,
  MarkAreaComponent,
]);

export default echarts;
