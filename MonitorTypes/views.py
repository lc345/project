from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.template import loader
from MonitorTypes.models import MonitorTypes, Resume
from MonitorTypes.models import TypeName
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView

# Create your views here.

def monitorlist(request):
    monitor_list = MonitorTypes.objects.order_by('monitor_type')
    template = loader.get_template('monitorlist.html')
    context = {'monitor_list': monitor_list}

    for monitor in monitor_list:
        monitor.monitor_type = TypeName[monitor.monitor_type][1]

    return HttpResponse(template.render(context))

def detail(request, monitor_id):
    try:
        monitor = MonitorTypes.objects.get(pk=monitor_id)
        monitor.monitor_type = TypeName[monitor.monitor_type][1]
    except  MonitorTypes.DoesNotExist:
        raise Http404("not exist")
    
    print(monitor)
    return render(request, 'monitor.html', {'monitor': monitor})


class ResumeDetailView(DetailView):
    """   简历详情页    """
    model = Resume
    template_name = 'resume_detail.html'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """    简历职位页面  """
    template_name = 'resume_form.html'
    success_url = '/monitorlist/'
    model = Resume
    fields = ["username", "city", "phone",
        "email", "apply_position", "gender",
        "bachelor_school", "master_school", "major", "degree", "picture", "attachment",
        "candidate_introduction", "work_experience", "project_experience"]


    # def post(self, request, *args, **kwargs):
    #     form = ResumeForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)

    #     return render(request, self.template_name, {'form': form})

    ### 从 URL 请求参数带入默认值
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())