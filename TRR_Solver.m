function rslt = TRR_Solver(lb, ub)
disp("++++++++++++++ Matlab Optimization Toolbox ++++++++++++");
disp("---------- Algorithm: trust-region-reflective----------");
A = []; % Linear inequality constraint A
b = []; % Linear inequality constraint b
Aeq = []; % Linear equality constraint A
beq = []; % Linear equality constraint b
nonlcon = []; % Nonlinear constraint
x0 = lb; % Initial point at the lower bound
options = optimoptions('fmincon','Algorithm','trust-region-reflective',...
    'SpecifyObjectiveGradient',true,'HessianFcn','objective');
disp("Set options...");
[C,e,exitflag,output] = ...
   fmincon(@HelperFunc,x0,A,b,Aeq,beq,lb,ub,nonlcon,options);
rslt = [C, e];
disp("------------- Finish searching ----------------");
disp("C: ");
disp(C);
disp("e: ");
disp(e);
disp("Exitflag: ");
disp(exitflag);
disp("Constraint violation: ");
disp(output.constrviolation);
disp("-----------------------------------------------");
end

function [f, g, H] = HelperFunc(x)
% Evaluate the function
% config = [41.9, 41.9, x(1), 27.49, 27.49, x(2)];
% x = config;
f = py.ModeID.f(x);
f = double(f);

% Evaluate the gradient
if nargout > 1
    g = py.ModeID.getGradient(@py.ModeID.f, x);
    g = double(g);
end

if nargout > 2
    H = py.ModeID.getHessian(@py.ModeID.f, x);
    H = double(H);
end
end