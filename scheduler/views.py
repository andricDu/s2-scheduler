# Copyright (c) 2016 The Ontario Institute for Cancer Research. All rights reserved.
#
# This program and the accompanying materials are made available under the terms of the GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from scheduler.models import *


"""
Atomic Requests have been set to true app wide. Entire views are run as single
transactions against the database.
"""


def index(request):
    return HttpResponse("Sample Scheduler")


def headers_check(func):
    """
    Decorator for checking the X-IP in the header.
    :param func: decorated view
    :return: bad request or response from view.
    """
    def check(request):
        if (request.META is None) or ('HTTP_X_IP' not in request.META):
            return HttpResponseBadRequest('Must set X-IP in header.')
        else:
            if request.method == 'POST' and ('HTTP_X_UUID' not in request.META):
                return HttpResponseBadRequest('Must set X-UUID in header.')
            return func(request)
    return check


@headers_check
def get_sample(request):
    """
    Move sample from queued to in progress.
    """
    if not request.method == 'GET':
        return HttpResponseBadRequest('Only GET requests are allowed.')

    sample = QueuedSample.objects.first()
    if sample is None:
        return HttpResponse("The sample queue is empty.")

    sample_id = sample.sample_id
    in_progress = InProgressSample(sample_id=sample_id, ip=request.META['HTTP_X_IP'])
    in_progress.save()
    sample.delete()

    return HttpResponse(sample_id)


@headers_check
def finish_sample(request):
    """
    Move sample from in progress to finished.
    """
    if not request.method == 'POST':
        return HttpResponseBadRequest('Only POST requests are allowed.')

    ip = request.META['HTTP_X_IP']
    sample_id = request.META['HTTP_X_UUID']

    in_progress = InProgressSample.objects.get(sample_id=sample_id)
    if in_progress.ip != ip:
        return HttpResponseNotAllowed('This IP is not registered to this sample.')

    finished_sample = FinishedSample(sample_id=sample_id)
    finished_sample.save()
    in_progress.delete()

    return HttpResponse('Sample {} has been registered as finished.'.format(sample_id))
