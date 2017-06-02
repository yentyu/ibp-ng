
% r_dist(): function for writing distance restraints.
function r_dist (num1, res1, num2, res2, d0, da, db)
  printf(['assign ', ...
          '(resid %2d and name %2s) ', ...
          '(resid %2d and name %2s) ', ...
          '%8.3f %8.3f %8.3f\n'], num1, res1, num2, res2, d0, da, db);
end

