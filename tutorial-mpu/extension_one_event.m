% Table 4 sensitivity analysis: omit the largest absolute MPU-change event.
% Bauer, Lakdawala and Mueller (2022), Market-Based Monetary Policy Uncertainty.
% Same 10-year nominal Treasury yield specification and HC0 standard errors.

scriptDir = fileparts(mfilename('fullpath'));
addpath(fullfile(scriptDir, 'aux_files'));
D = readtable(fullfile(scriptDir, 'data', 'tab4data.csv'));

% The date column may be imported as datetime or text.
eventDates = D.Time;
if ~isdatetime(eventDates)
    eventDates = datetime(string(eventDates), 'InputFormat', 'dd-MMM-yyyy');
end

omitDate = datetime(2011, 8, 9);
include = eventDates ~= omitDate;
assert(height(D) == 197, 'Expected 197 observations in the original dataset.');
assert(sum(~include) == 1, 'Expected exactly one observation on 9 August 2011.');
[~, maximumIndex] = max(abs(D.mpu));
assert(eventDates(maximumIndex) == omitDate, 'The selected event is not the largest absolute MPU change.');

% Reproduce the authors' Table 4, 10-year yield, specification 2.
regressionData = table(D.mps, D.mpu, D.dSVENY10, ...
    'VariableNames', {'mps', 'mpu', 'yield10'});
[fullModel, fullSE, ~, ~, fullT] = olsrob_nodisp(regressionData);
[omitModel, omitSE, ~, ~, omitT] = olsrob_nodisp(regressionData(include, :));

% The MPU parameter is identified by name, not by a hardcoded position.
fullIdx = find(strcmp(fullModel.CoefficientNames, 'mpu'));
omitIdx = find(strcmp(omitModel.CoefficientNames, 'mpu'));
assert(isscalar(fullIdx) && isscalar(omitIdx), 'MPU coefficient not found.');

Specification = ["Original specification"; "Exclude 9 August 2011"];
N = [fullModel.NumObservations; omitModel.NumObservations];
MPU_coefficient = [fullModel.Coefficients.Estimate(fullIdx); omitModel.Coefficients.Estimate(omitIdx)];
HC0_robust_SE = [fullSE(fullIdx); omitSE(omitIdx)];
Robust_t_statistic = [fullT(fullIdx); omitT(omitIdx)];
R_squared = [fullModel.Rsquared.Ordinary; omitModel.Rsquared.Ordinary];
extension_results = table(Specification, N, MPU_coefficient, HC0_robust_SE, Robust_t_statistic, R_squared);

disp(extension_results)
fprintf('Change in MPU coefficient: %.1f%%\n', ...
    100*(MPU_coefficient(2)/MPU_coefficient(1)-1));
writetable(extension_results, fullfile(scriptDir, 'results', 'extension_results.csv'));
